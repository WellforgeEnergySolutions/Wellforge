/*!
 * wf3d.js - a small, dependency-free WebGL engine for the Wellforge website.
 *
 * Everything the 3D scenes need and nothing they don't: 4x4 maths, a handful of
 * procedural geometry builders (lathe, cylinder, box, torus, sphere), a single
 * physically-flavoured shader, and a drag-to-orbit camera. No external library,
 * so the site works offline and straight off the filesystem.
 *
 * Geometry is baked into as few buffers as possible - one per animated part -
 * which keeps a full drilling rig at a couple of draw calls per frame.
 */
(function (global) {
  'use strict';

  /* =====================================================================
     Matrix / vector maths  (column-major, matching WebGL)
     ===================================================================== */
  var M4 = {
    ident: function () {
      return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
    },

    mul: function (a, b) {            // returns a * b
      var o = new Float32Array(16), i, j, k, s;
      for (i = 0; i < 4; i++) {
        for (j = 0; j < 4; j++) {
          s = 0;
          for (k = 0; k < 4; k++) s += a[k * 4 + j] * b[i * 4 + k];
          o[i * 4 + j] = s;
        }
      }
      return o;
    },

    chain: function () {              // chain(a, b, c) === a * b * c
      var o = arguments[0], i;
      for (i = 1; i < arguments.length; i++) o = M4.mul(o, arguments[i]);
      return o;
    },

    trans: function (x, y, z) {
      return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, x,y,z,1]);
    },

    scale: function (x, y, z) {
      if (y === undefined) { y = x; z = x; }
      return new Float32Array([x,0,0,0, 0,y,0,0, 0,0,z,0, 0,0,0,1]);
    },

    rotX: function (t) {
      var c = Math.cos(t), s = Math.sin(t);
      return new Float32Array([1,0,0,0, 0,c,s,0, 0,-s,c,0, 0,0,0,1]);
    },

    rotY: function (t) {
      var c = Math.cos(t), s = Math.sin(t);
      return new Float32Array([c,0,-s,0, 0,1,0,0, s,0,c,0, 0,0,0,1]);
    },

    rotZ: function (t) {
      var c = Math.cos(t), s = Math.sin(t);
      return new Float32Array([c,s,0,0, -s,c,0,0, 0,0,1,0, 0,0,0,1]);
    },

    persp: function (fovy, aspect, near, far) {
      var f = 1 / Math.tan(fovy / 2), nf = 1 / (near - far);
      return new Float32Array([
        f / aspect, 0, 0, 0,
        0, f, 0, 0,
        0, 0, (far + near) * nf, -1,
        0, 0, 2 * far * near * nf, 0
      ]);
    },

    lookAt: function (eye, target, up) {
      var z = V3.norm(V3.sub(eye, target));
      var x = V3.norm(V3.cross(up, z));
      var y = V3.cross(z, x);
      return new Float32Array([
        x[0], y[0], z[0], 0,
        x[1], y[1], z[1], 0,
        x[2], y[2], z[2], 0,
        -V3.dot(x, eye), -V3.dot(y, eye), -V3.dot(z, eye), 1
      ]);
    },

    /* Inverse-transpose of the upper 3x3, for transforming normals. */
    normalMat: function (m) {
      var a00 = m[0], a01 = m[1], a02 = m[2],
          a10 = m[4], a11 = m[5], a12 = m[6],
          a20 = m[8], a21 = m[9], a22 = m[10];
      var b01 =  a22 * a11 - a12 * a21,
          b11 = -a22 * a10 + a12 * a20,
          b21 =  a21 * a10 - a11 * a20;
      var det = a00 * b01 + a01 * b11 + a02 * b21;
      if (!det) return new Float32Array([1,0,0, 0,1,0, 0,0,1]);
      det = 1 / det;
      return new Float32Array([
        b01 * det,
        (-a22 * a01 + a02 * a21) * det,
        ( a12 * a01 - a02 * a11) * det,
        b11 * det,
        ( a22 * a00 - a02 * a20) * det,
        (-a12 * a00 + a02 * a10) * det,
        b21 * det,
        (-a21 * a00 + a01 * a20) * det,
        ( a11 * a00 - a01 * a10) * det
      ]);
    }
  };

  var V3 = {
    sub:  function (a, b) { return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]; },
    cross:function (a, b) { return [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]; },
    dot:  function (a, b) { return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]; },
    norm: function (a) {
      var l = Math.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2]) || 1;
      return [a[0]/l, a[1]/l, a[2]/l];
    }
  };

  /* =====================================================================
     Geometry builders
     Each returns { p: positions[], n: normals[], i: indices[] }
     ===================================================================== */
  var TAU = Math.PI * 2;

  function emptyGeo() { return { p: [], n: [], i: [] }; }

  /**
   * Surface of revolution around the Y axis.
   * profile: [[radius, y], ...] read bottom-to-top.
   * Repeat a profile point to force a hard crease at that ring.
   */
  function lathe(profile, segs, capBottom, capTop) {
    segs = segs || 32;
    var g = emptyGeo(), rings = profile.length, i, k, ang, cs, sn;

    // Per-ring 2D normals, averaged across the two adjoining segments.
    var rn = [];
    for (k = 0; k < rings; k++) {
      var nx = 0, ny = 0, cnt = 0, dr, dy, l;
      if (k > 0) {
        dr = profile[k][0] - profile[k-1][0];
        dy = profile[k][1] - profile[k-1][1];
        l = Math.sqrt(dr*dr + dy*dy);
        if (l > 1e-9) { nx += dy / l; ny += -dr / l; cnt++; }
      }
      if (k < rings - 1) {
        dr = profile[k+1][0] - profile[k][0];
        dy = profile[k+1][1] - profile[k][1];
        l = Math.sqrt(dr*dr + dy*dy);
        if (l > 1e-9) { nx += dy / l; ny += -dr / l; cnt++; }
      }
      if (!cnt) { nx = 1; ny = 0; }
      l = Math.sqrt(nx*nx + ny*ny) || 1;
      rn.push([nx / l, ny / l]);
    }

    for (k = 0; k < rings; k++) {
      for (i = 0; i <= segs; i++) {
        ang = i / segs * TAU;
        cs = Math.cos(ang); sn = Math.sin(ang);
        g.p.push(profile[k][0] * cs, profile[k][1], profile[k][0] * sn);
        g.n.push(rn[k][0] * cs, rn[k][1], rn[k][0] * sn);
      }
    }
    for (k = 0; k < rings - 1; k++) {
      for (i = 0; i < segs; i++) {
        var a = k * (segs + 1) + i, b = a + segs + 1;
        g.i.push(a, b, a + 1, a + 1, b, b + 1);
      }
    }

    if (capBottom && profile[0][0] > 1e-6) addDisc(g, profile[0][0], profile[0][1], segs, -1);
    if (capTop && profile[rings-1][0] > 1e-6) addDisc(g, profile[rings-1][0], profile[rings-1][1], segs, 1);
    return g;
  }

  function addDisc(g, r, y, segs, dir) {
    var base = g.p.length / 3, i, ang;
    g.p.push(0, y, 0); g.n.push(0, dir, 0);
    for (i = 0; i <= segs; i++) {
      ang = i / segs * TAU;
      g.p.push(r * Math.cos(ang), y, r * Math.sin(ang));
      g.n.push(0, dir, 0);
    }
    for (i = 0; i < segs; i++) {
      if (dir > 0) g.i.push(base, base + 1 + i, base + 2 + i);
      else         g.i.push(base, base + 2 + i, base + 1 + i);
    }
  }

  /** Straight or tapered tube; y runs from -h/2 to +h/2. */
  function cylinder(rBottom, rTop, h, segs, caps) {
    var p = [[rBottom, -h / 2], [rTop, h / 2]];
    return lathe(p, segs || 32, caps !== false, caps !== false);
  }

  /** Hollow pipe with a visible wall thickness. */
  function tube(rOuter, rInner, h, segs) {
    var p = [
      [rInner, -h / 2], [rOuter, -h / 2], [rOuter, -h / 2],
      [rOuter,  h / 2], [rOuter,  h / 2], [rInner,  h / 2],
      [rInner,  h / 2], [rInner, -h / 2]
    ];
    return lathe(p, segs || 40, false, false);
  }

  function box(w, h, d) {
    var x = w / 2, y = h / 2, z = d / 2;
    var g = emptyGeo();
    var faces = [
      [[ x,-y, z],[ x,-y,-z],[ x, y,-z],[ x, y, z], [ 1, 0, 0]],
      [[-x,-y,-z],[-x,-y, z],[-x, y, z],[-x, y,-z], [-1, 0, 0]],
      [[-x, y, z],[ x, y, z],[ x, y,-z],[-x, y,-z], [ 0, 1, 0]],
      [[-x,-y,-z],[ x,-y,-z],[ x,-y, z],[-x,-y, z], [ 0,-1, 0]],
      [[-x,-y, z],[ x,-y, z],[ x, y, z],[-x, y, z], [ 0, 0, 1]],
      [[ x,-y,-z],[-x,-y,-z],[-x, y,-z],[ x, y,-z], [ 0, 0,-1]]
    ];
    faces.forEach(function (f) {
      var base = g.p.length / 3, j;
      for (j = 0; j < 4; j++) {
        g.p.push(f[j][0], f[j][1], f[j][2]);
        g.n.push(f[4][0], f[4][1], f[4][2]);
      }
      g.i.push(base, base + 1, base + 2, base, base + 2, base + 3);
    });
    return g;
  }

  function torus(R, r, segsMajor, segsMinor) {
    segsMajor = segsMajor || 40; segsMinor = segsMinor || 16;
    var g = emptyGeo(), i, j;
    for (i = 0; i <= segsMajor; i++) {
      var u = i / segsMajor * TAU, cu = Math.cos(u), su = Math.sin(u);
      for (j = 0; j <= segsMinor; j++) {
        var v = j / segsMinor * TAU, cv = Math.cos(v), sv = Math.sin(v);
        g.p.push((R + r * cv) * cu, r * sv, (R + r * cv) * su);
        g.n.push(cv * cu, sv, cv * su);
      }
    }
    for (i = 0; i < segsMajor; i++) {
      for (j = 0; j < segsMinor; j++) {
        var a = i * (segsMinor + 1) + j, b = a + segsMinor + 1;
        g.i.push(a, b, a + 1, a + 1, b, b + 1);
      }
    }
    return g;
  }

  function sphere(r, segs, rings) {
    segs = segs || 28; rings = rings || 18;
    var g = emptyGeo(), i, j;
    for (j = 0; j <= rings; j++) {
      var phi = j / rings * Math.PI, sp = Math.sin(phi), cp = Math.cos(phi);
      for (i = 0; i <= segs; i++) {
        var th = i / segs * TAU, st = Math.sin(th), ct = Math.cos(th);
        var nx = sp * ct, ny = cp, nz = sp * st;
        g.p.push(r * nx, r * ny, r * nz);
        g.n.push(nx, ny, nz);
      }
    }
    for (j = 0; j < rings; j++) {
      for (i = 0; i < segs; i++) {
        var a = j * (segs + 1) + i, b = a + segs + 1;
        g.i.push(a, b, a + 1, a + 1, b, b + 1);
      }
    }
    return g;
  }

  /** A cone with a rounded tip - used for drill-bit teeth and inserts. */
  function stud(r, h, segs) {
    return lathe([[0, 0], [r * 0.92, h * 0.18], [r * 0.55, h * 0.72], [0, h]], segs || 10, true, false);
  }

  /* =====================================================================
     Builder - bakes many transformed pieces into one interleaved buffer
     ===================================================================== */
  function hexToRGB(hex) {
    if (typeof hex !== 'string') return hex;                 // already [r,g,b]
    var h = hex.replace('#', '');
    if (h.length === 3) h = h[0]+h[0]+h[1]+h[1]+h[2]+h[2];
    var n = parseInt(h, 16);
    // sRGB -> approximately linear, so the shader's tone-map behaves
    return [
      Math.pow(((n >> 16) & 255) / 255, 2.2),
      Math.pow(((n >>  8) & 255) / 255, 2.2),
      Math.pow(( n        & 255) / 255, 2.2)
    ];
  }

  function Builder() {
    this.v = [];      // interleaved: px py pz nx ny nz r g b metal rough
    this.i = [];
    this.count = 0;
  }

  /**
   * add(geometry, { m: matrix, color: '#rrggbb', metal: 0..1, rough: 0..1 })
   */
  Builder.prototype.add = function (g, o) {
    o = o || {};
    var m = o.m || M4.ident();
    var nm = M4.normalMat(m);
    var col = hexToRGB(o.color || '#8892a4');
    var metal = o.metal === undefined ? 0.85 : o.metal;
    var rough = o.rough === undefined ? 0.38 : o.rough;
    var base = this.count, k, n = g.p.length / 3;

    for (k = 0; k < n; k++) {
      var x = g.p[k*3], y = g.p[k*3+1], z = g.p[k*3+2];
      this.v.push(
        m[0]*x + m[4]*y + m[8]*z  + m[12],
        m[1]*x + m[5]*y + m[9]*z  + m[13],
        m[2]*x + m[6]*y + m[10]*z + m[14]
      );
      var a = g.n[k*3], b = g.n[k*3+1], c = g.n[k*3+2];
      var nx = nm[0]*a + nm[3]*b + nm[6]*c,
          ny = nm[1]*a + nm[4]*b + nm[7]*c,
          nz = nm[2]*a + nm[5]*b + nm[8]*c;
      var l = Math.sqrt(nx*nx + ny*ny + nz*nz) || 1;
      this.v.push(nx/l, ny/l, nz/l, col[0], col[1], col[2], metal, rough);
    }
    for (k = 0; k < g.i.length; k++) this.i.push(base + g.i[k]);
    this.count += n;
    return this;
  };

  /* Repeat a piece around the Y axis - bolt circles, teeth rows, lattice legs. */
  Builder.prototype.ring = function (g, n, radius, opts, extra) {
    opts = opts || {};
    for (var k = 0; k < n; k++) {
      var a = k / n * TAU;
      var m = M4.chain(M4.rotY(a), M4.trans(radius, 0, 0), extra ? extra(k, a) : M4.ident());
      var o = {}, key;
      for (key in opts) if (opts.hasOwnProperty(key)) o[key] = opts[key];
      o.m = opts.m ? M4.mul(opts.m, m) : m;
      this.add(g, o);
    }
    return this;
  };

  /* =====================================================================
     Shaders
     ===================================================================== */
  var VERT = [
    'attribute vec3 aPos;',
    'attribute vec3 aNrm;',
    'attribute vec3 aCol;',
    'attribute vec2 aMat;',
    'uniform mat4 uProj, uView, uModel;',
    'uniform mat3 uNrmMat;',
    'varying vec3 vN, vW, vC;',
    'varying vec2 vM;',
    'void main() {',
    '  vec4 wp = uModel * vec4(aPos, 1.0);',
    '  vW = wp.xyz;',
    '  vN = normalize(uNrmMat * aNrm);',
    '  vC = aCol; vM = aMat;',
    '  gl_Position = uProj * uView * wp;',
    '}'
  ].join('\n');

  var FRAG = [
    'precision highp float;',
    'varying vec3 vN, vW, vC;',
    'varying vec2 vM;',
    'uniform vec3 uCam;',
    'uniform vec3 uL1D, uL1C, uL2D, uL2C, uL3D, uL3C;',
    'uniform vec3 uSky, uGround, uRim;',
    'uniform float uRimPow, uExposure;',
    'const float PI = 3.14159265;',

    'vec3 fresnel(vec3 f0, float u) { return f0 + (1.0 - f0) * pow(1.0 - u, 5.0); }',

    'float ggx(float NoH, float a) {',
    '  float a2 = a * a;',
    '  float d = NoH * NoH * (a2 - 1.0) + 1.0;',
    '  return a2 / max(PI * d * d, 1e-6);',
    '}',

    'float smithV(float NoV, float NoL, float a) {',
    '  float a2 = a * a;',
    '  float gv = NoL * sqrt(NoV * NoV * (1.0 - a2) + a2);',
    '  float gl = NoV * sqrt(NoL * NoL * (1.0 - a2) + a2);',
    '  return 0.5 / max(gv + gl, 1e-5);',
    '}',

    'vec3 lightContrib(vec3 N, vec3 V, vec3 L, vec3 lc, vec3 alb, float metal, float rough) {',
    '  vec3 H = normalize(V + L);',
    '  float NoL = max(dot(N, L), 0.0);',
    '  if (NoL <= 0.0) return vec3(0.0);',
    '  float NoV = max(dot(N, V), 1e-4);',
    '  float NoH = max(dot(N, H), 0.0);',
    '  float VoH = max(dot(V, H), 0.0);',
    '  float a = max(rough * rough, 0.003);',
    '  vec3 f0 = mix(vec3(0.04), alb, metal);',
    '  vec3 F = fresnel(f0, VoH);',
    '  vec3 spec = F * ggx(NoH, a) * smithV(NoV, NoL, a);',
    '  vec3 kd = (1.0 - F) * (1.0 - metal);',
    '  return (kd * alb / PI + spec) * lc * NoL;',
    '}',

    // Filmic curve so the gold highlights roll off instead of clipping.
    'vec3 tonemap(vec3 x) {',
    '  x *= uExposure;',
    '  vec3 a = x * (2.51 * x + 0.03);',
    '  vec3 b = x * (2.43 * x + 0.59) + 0.14;',
    '  return clamp(a / b, 0.0, 1.0);',
    '}',

    'void main() {',
    '  vec3 N = normalize(vN);',
    '  vec3 V = normalize(uCam - vW);',
    '  if (!gl_FrontFacing) N = -N;',
    '  float metal = vM.x;',
    '  float rough = clamp(vM.y, 0.03, 1.0);',
    '  vec3 alb = vC;',

    '  vec3 col = vec3(0.0);',
    '  col += lightContrib(N, V, normalize(uL1D), uL1C, alb, metal, rough);',
    '  col += lightContrib(N, V, normalize(uL2D), uL2C, alb, metal, rough);',
    '  col += lightContrib(N, V, normalize(uL3D), uL3C, alb, metal, rough);',

    // Hemisphere ambient stands in for an environment map.
    '  float hemi = N.y * 0.5 + 0.5;',
    '  vec3 amb = mix(uGround, uSky, hemi);',
    '  float NoV = max(dot(N, V), 1e-4);',
    '  vec3 f0 = mix(vec3(0.04), alb, metal);',
    '  vec3 specAmb = fresnel(f0, NoV) * (1.0 - rough * 0.85);',
    '  col += amb * alb * (1.0 - metal * 0.75) + amb * specAmb * 1.35;',

    // Warm rim separates the metal from a dark page background.
    '  col += uRim * pow(1.0 - NoV, uRimPow) * (0.35 + metal * 0.65);',

    '  gl_FragColor = vec4(pow(tonemap(col), vec3(1.0 / 2.2)), 1.0);',
    '}'
  ].join('\n');

  /* =====================================================================
     Scene
     ===================================================================== */
  function compile(gl, type, src) {
    var s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      throw new Error('wf3d shader: ' + gl.getShaderInfoLog(s));
    }
    return s;
  }

  /**
   * new Scene(canvas, options)
   *   options.camera   [x, y, z] eye position
   *   options.target   [x, y, z] look-at point
   *   options.fov      vertical field of view in degrees
   *   options.autoSpin radians per second of idle rotation
   *   options.orbit    false to disable drag-to-rotate
   *   options.maxPitch clamp for vertical dragging (radians)
   */
  function Scene(canvas, options) {
    options = options || {};
    var gl = canvas.getContext('webgl', {
      antialias: true, alpha: true, premultipliedAlpha: false,
      depth: true, powerPreference: 'high-performance'
    }) || canvas.getContext('experimental-webgl', { antialias: true, alpha: true });
    if (!gl) throw new Error('WebGL unavailable');

    this.gl = gl;
    this.canvas = canvas;
    this.opts = options;
    this.parts = [];
    this.time = 0;
    this.running = false;
    this.visible = true;

    this.yaw = options.yaw || 0;
    this.pitch = options.pitch || 0;
    this.yawVel = 0;
    this.pitchVel = 0;
    this.dragging = false;
    this.pointerX = 0;
    this.pointerY = 0;      // -1..1 parallax, driven by the pointer over the canvas
    this.parallax = options.parallax === undefined ? 0.12 : options.parallax;

    var prog = gl.createProgram();
    gl.attachShader(prog, compile(gl, gl.VERTEX_SHADER, VERT));
    gl.attachShader(prog, compile(gl, gl.FRAGMENT_SHADER, FRAG));
    gl.bindAttribLocation(prog, 0, 'aPos');
    gl.bindAttribLocation(prog, 1, 'aNrm');
    gl.bindAttribLocation(prog, 2, 'aCol');
    gl.bindAttribLocation(prog, 3, 'aMat');
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      throw new Error('wf3d link: ' + gl.getProgramInfoLog(prog));
    }
    this.prog = prog;
    this.u = {};
    ['uProj','uView','uModel','uNrmMat','uCam','uL1D','uL1C','uL2D','uL2C','uL3D','uL3C',
     'uSky','uGround','uRim','uRimPow','uExposure'].forEach(function (n) {
      this.u[n] = gl.getUniformLocation(prog, n);
    }, this);

    gl.enable(gl.DEPTH_TEST);
    gl.enable(gl.CULL_FACE);
    gl.cullFace(gl.BACK);

    this.lights = options.lights || Scene.DEFAULT_LIGHTS;
    this._bindPointer();
    this._resize();
  }

  /* Studio three-point rig: warm key, cool fill, gold kicker. */
  Scene.DEFAULT_LIGHTS = {
    l1: { dir: [ 0.50,  0.82,  0.58], col: [2.35, 2.34, 2.30] },
    l2: { dir: [-0.74,  0.24,  0.46], col: [0.46, 0.60, 0.98] },
    l3: { dir: [ 0.16, -0.48, -0.82], col: [1.55, 1.02, 0.36] },
    sky:    [0.21, 0.25, 0.34],
    ground: [0.05, 0.06, 0.09],
    rim:    [0.50, 0.36, 0.13],
    rimPow: 3.0,
    exposure: 1.05
  };

  /**
   * addPart(builder, updateFn)
   * updateFn(time, scene) -> model matrix; omit for a static part.
   */
  Scene.prototype.addPart = function (builder, update) {
    var gl = this.gl;
    var vbo = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(builder.v), gl.STATIC_DRAW);

    var big = builder.count > 65535;
    var ext = big ? gl.getExtension('OES_element_index_uint') : null;
    if (big && !ext) throw new Error('wf3d: part exceeds 16-bit index range');
    var ibo = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
      big ? new Uint32Array(builder.i) : new Uint16Array(builder.i), gl.STATIC_DRAW);

    this.parts.push({
      vbo: vbo, ibo: ibo, n: builder.i.length,
      type: big ? gl.UNSIGNED_INT : gl.UNSIGNED_SHORT,
      update: update || null
    });
    return this;
  };

  Scene.prototype._resize = function () {
    var c = this.canvas;
    var dpr = Math.min(global.devicePixelRatio || 1, 2);
    var w = Math.max(1, Math.round(c.clientWidth * dpr));
    var h = Math.max(1, Math.round(c.clientHeight * dpr));
    if (c.width !== w || c.height !== h) {
      c.width = w; c.height = h;
      this.gl.viewport(0, 0, w, h);
    }
    this.aspect = c.clientWidth / Math.max(1, c.clientHeight);
  };

  Scene.prototype._bindPointer = function () {
    var self = this, c = this.canvas;
    var lastX = 0, lastY = 0, touchStart = null, decided = null;

    function down(x, y) { self.dragging = true; lastX = x; lastY = y; c.classList.add('is-grabbing'); }
    function move(x, y) {
      var dx = x - lastX, dy = y - lastY;
      lastX = x; lastY = y;
      self.yawVel += dx * 0.006;
      self.pitchVel += dy * 0.004;
    }
    function up() { self.dragging = false; c.classList.remove('is-grabbing'); }

    if (this.opts.orbit !== false) {
      c.addEventListener('mousedown', function (e) { e.preventDefault(); down(e.clientX, e.clientY); });
      global.addEventListener('mousemove', function (e) { if (self.dragging) move(e.clientX, e.clientY); });
      global.addEventListener('mouseup', up);

      // On touch, only claim the gesture once it is clearly horizontal -
      // a vertical swipe must still scroll the page.
      c.addEventListener('touchstart', function (e) {
        var t = e.touches[0];
        touchStart = [t.clientX, t.clientY];
        decided = null;
        lastX = t.clientX; lastY = t.clientY;
      }, { passive: true });

      c.addEventListener('touchmove', function (e) {
        var t = e.touches[0];
        if (decided === null && touchStart) {
          var dx = Math.abs(t.clientX - touchStart[0]);
          var dy = Math.abs(t.clientY - touchStart[1]);
          if (dx + dy > 8) decided = dx > dy * 1.2;
          if (decided) self.dragging = true;
        }
        if (decided) { e.preventDefault(); move(t.clientX, t.clientY); }
      }, { passive: false });

      c.addEventListener('touchend', function () { decided = null; up(); }, { passive: true });
    }

    // Gentle parallax as the pointer crosses the canvas.
    c.addEventListener('mousemove', function (e) {
      var r = c.getBoundingClientRect();
      self.pointerX = ((e.clientX - r.left) / r.width) * 2 - 1;
      self.pointerY = ((e.clientY - r.top) / r.height) * 2 - 1;
    });
    c.addEventListener('mouseleave', function () { self.pointerX = 0; self.pointerY = 0; });
  };

  Scene.prototype.render = function (dt) {
    var gl = this.gl, o = this.opts, L = this.lights;
    this._resize();
    this.time += dt;

    // Idle spin, plus whatever momentum the last drag left behind.
    if (!this.dragging) this.yaw += (o.autoSpin === undefined ? 0.22 : o.autoSpin) * dt;
    this.yaw += this.yawVel;
    this.pitch += this.pitchVel;
    this.yawVel *= 0.90;
    this.pitchVel *= 0.90;
    var maxPitch = o.maxPitch === undefined ? 0.62 : o.maxPitch;
    this.pitch = Math.max(-maxPitch, Math.min(maxPitch, this.pitch));

    var eye = (o.camera || [0, 1.6, 6.4]).slice();
    var target = o.target || [0, 0, 0];
    if (this.parallax) {
      eye[0] += this.pointerX * this.parallax * 1.6;
      eye[1] -= this.pointerY * this.parallax;
    }

    var proj = M4.persp((o.fov || 34) * Math.PI / 180, this.aspect, 0.05, 200);
    var view = M4.lookAt(eye, target, [0, 1, 0]);
    var spin = M4.mul(M4.rotX(this.pitch), M4.rotY(this.yaw));

    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
    gl.useProgram(this.prog);

    gl.uniformMatrix4fv(this.u.uProj, false, proj);
    gl.uniformMatrix4fv(this.u.uView, false, view);
    gl.uniform3fv(this.u.uCam, new Float32Array(eye));
    gl.uniform3fv(this.u.uL1D, new Float32Array(L.l1.dir));
    gl.uniform3fv(this.u.uL1C, new Float32Array(L.l1.col));
    gl.uniform3fv(this.u.uL2D, new Float32Array(L.l2.dir));
    gl.uniform3fv(this.u.uL2C, new Float32Array(L.l2.col));
    gl.uniform3fv(this.u.uL3D, new Float32Array(L.l3.dir));
    gl.uniform3fv(this.u.uL3C, new Float32Array(L.l3.col));
    gl.uniform3fv(this.u.uSky, new Float32Array(L.sky));
    gl.uniform3fv(this.u.uGround, new Float32Array(L.ground));
    gl.uniform3fv(this.u.uRim, new Float32Array(L.rim));
    gl.uniform1f(this.u.uRimPow, L.rimPow === undefined ? 3.2 : L.rimPow);
    gl.uniform1f(this.u.uExposure, L.exposure === undefined ? 1 : L.exposure);

    var stride = 11 * 4;
    for (var k = 0; k < this.parts.length; k++) {
      var part = this.parts[k];
      var model = part.update ? part.update(this.time, this) : M4.ident();
      model = M4.mul(spin, model);

      gl.bindBuffer(gl.ARRAY_BUFFER, part.vbo);
      gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 3, gl.FLOAT, false, stride, 0);
      gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1, 3, gl.FLOAT, false, stride, 12);
      gl.enableVertexAttribArray(2); gl.vertexAttribPointer(2, 3, gl.FLOAT, false, stride, 24);
      gl.enableVertexAttribArray(3); gl.vertexAttribPointer(3, 2, gl.FLOAT, false, stride, 36);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, part.ibo);

      gl.uniformMatrix4fv(this.u.uModel, false, model);
      gl.uniformMatrix3fv(this.u.uNrmMat, false, M4.normalMat(model));
      gl.drawElements(gl.TRIANGLES, part.n, part.type, 0);
    }

    // Let the page know something is actually on screen. Callers use this to
    // swap the still illustration for the canvas, so a context that never
    // paints leaves the illustration in place rather than an empty box.
    if (!this.rendered) {
      this.rendered = true;
      if (o.onFirstFrame) o.onFirstFrame(this);
    }
  };

  /** Start the loop, pausing whenever the canvas scrolls out of view. */
  Scene.prototype.start = function () {
    if (this.running) return this;
    this.running = true;
    var self = this, last = 0;

    if (global.IntersectionObserver) {
      var io = new IntersectionObserver(function (entries) {
        self.visible = entries[0].isIntersecting;
        if (self.visible) last = 0;
      }, { rootMargin: '120px' });
      io.observe(this.canvas);
    }

    function frame(now) {
      if (!self.running) return;
      global.requestAnimationFrame(frame);
      if (!self.visible || global.document.hidden) return;
      if (!last) last = now;
      var dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      self.render(dt);
    }
    global.requestAnimationFrame(frame);
    return this;
  };

  Scene.prototype.stop = function () { this.running = false; };

  /* =====================================================================
     Exports
     ===================================================================== */
  global.WF3D = {
    M4: M4, V3: V3, Builder: Builder, Scene: Scene, TAU: TAU,
    geo: {
      lathe: lathe, cylinder: cylinder, tube: tube, box: box,
      torus: torus, sphere: sphere, stud: stud
    },
    supported: (function () {
      try {
        var c = document.createElement('canvas');
        return !!(global.WebGLRenderingContext &&
                 (c.getContext('webgl') || c.getContext('experimental-webgl')));
      } catch (e) { return false; }
    })()
  };
})(window);
