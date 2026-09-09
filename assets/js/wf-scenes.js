/*!
 * wf-scenes.js - the oilfield hardware that wf3d.js draws.
 *
 * Every model here is generated from primitives at page load - there are no
 * mesh files to download. Each entry declares its own camera framing and a
 * build() that pushes one baked buffer per independently animated part.
 *
 *   land rig .......... homepage hero
 *   tricone / pdc ..... drill bits
 *   packer ............ downhole completion tools
 *   casing ............ steel and tubular products
 *   gears ............. plant, machinery and industrial components
 *   mudmotor .......... drilling fluids, chemicals and consumables
 *   tree .............. subsea, offshore and onshore equipment
 *   valve ............. services
 */
(function (global) {
  'use strict';

  var WF = global.WF3D;
  if (!WF) return;

  var M4 = WF.M4, G = WF.geo, TAU = WF.TAU;

  /* ---------------------------------------------------------------------
     Shared material palette
     --------------------------------------------------------------------- */
  var MAT = {
    steel:   { color: '#93a0b0', metal: 0.96, rough: 0.28 },
    steelD:  { color: '#6c7686', metal: 0.94, rough: 0.40 },
    steelL:  { color: '#c7d0da', metal: 0.95, rough: 0.18 },
    iron:    { color: '#59616e', metal: 0.82, rough: 0.58 },
    gold:    { color: '#D9A22B', metal: 1.00, rough: 0.22 },
    goldD:   { color: '#a87c22', metal: 1.00, rough: 0.32 },
    navy:    { color: '#3d5286', metal: 0.30, rough: 0.48 },
    navyD:   { color: '#2b3a5e', metal: 0.25, rough: 0.56 },
    rubber:  { color: '#2a2e37', metal: 0.02, rough: 0.86 },
    carbide: { color: '#e2e9f0', metal: 0.92, rough: 0.14 },
    copper:  { color: '#bd7a3e', metal: 1.00, rough: 0.28 },
    paint:   { color: '#cc5b31', metal: 0.20, rough: 0.52 }
  };

  /* Clone a material with overrides, so callers never mutate the palette. */
  function mat(base, extra) {
    var o = {}, k;
    for (k in base) if (base.hasOwnProperty(k)) o[k] = base[k];
    if (extra) for (k in extra) if (extra.hasOwnProperty(k)) o[k] = extra[k];
    return o;
  }

  /* ---------------------------------------------------------------------
     Extra geometry helpers built on top of the engine primitives
     --------------------------------------------------------------------- */

  /** Matrix that places a unit-Y box as a beam running from a to b. */
  function alignY(a, b) {
    var d = [b[0]-a[0], b[1]-a[1], b[2]-a[2]];
    var len = Math.sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2]) || 1e-6;
    var up = [d[0]/len, d[1]/len, d[2]/len];
    var ref = Math.abs(up[1]) > 0.985 ? [1, 0, 0] : [0, 1, 0];
    var right = WF.V3.norm(WF.V3.cross(ref, up));
    var fwd = WF.V3.cross(up, right);
    return {
      m: new Float32Array([
        right[0], right[1], right[2], 0,
        up[0],    up[1],    up[2],    0,
        fwd[0],   fwd[1],   fwd[2],   0,
        (a[0]+b[0])/2, (a[1]+b[1])/2, (a[2]+b[2])/2, 1
      ]),
      len: len
    };
  }

  /** Structural member between two points - the workhorse of the derrick. */
  function strut(bld, a, b, w, material) {
    var t = alignY(a, b);
    bld.add(G.box(w, t.len, w), mat(material, { m: t.m }));
  }

  /**
   * Extrude a star-shaped 2D outline (one that the origin can "see" all of)
   * along Z. Used for gear and sprocket profiles.
   */
  function extrudeStar(points, depth) {
    var g = { p: [], n: [], i: [] };
    var n = points.length, hz = depth / 2, i;

    // Side wall - flat-shaded per quad so the tooth flanks read crisply.
    for (i = 0; i < n; i++) {
      var a = points[i], b = points[(i + 1) % n];
      var ex = b[0] - a[0], ey = b[1] - a[1];
      var l = Math.sqrt(ex * ex + ey * ey) || 1;
      var nx = ey / l, ny = -ex / l;
      var base = g.p.length / 3;
      g.p.push(a[0], a[1], -hz,  b[0], b[1], -hz,  b[0], b[1], hz,  a[0], a[1], hz);
      g.n.push(nx, ny, 0, nx, ny, 0, nx, ny, 0, nx, ny, 0);
      g.i.push(base, base + 1, base + 2, base, base + 2, base + 3);
    }

    // Caps, fanned from the centre.
    [hz, -hz].forEach(function (z) {
      var dir = z > 0 ? 1 : -1;
      var base = g.p.length / 3;
      g.p.push(0, 0, z); g.n.push(0, 0, dir);
      for (i = 0; i < n; i++) {
        g.p.push(points[i][0], points[i][1], z);
        g.n.push(0, 0, dir);
      }
      for (i = 0; i < n; i++) {
        var a = base + 1 + i, b = base + 1 + ((i + 1) % n);
        if (dir > 0) g.i.push(base, a, b);
        else g.i.push(base, b, a);
      }
    });
    return g;
  }

  /** Spur-gear outline: trapezoidal teeth on a root circle. */
  function gearProfile(teeth, rRoot, rTip) {
    var pts = [], k, step = TAU / teeth;
    for (k = 0; k < teeth; k++) {
      var a = k * step;
      pts.push([rRoot * Math.cos(a), rRoot * Math.sin(a)]);
      pts.push([rRoot * Math.cos(a + step * 0.16), rRoot * Math.sin(a + step * 0.16)]);
      pts.push([rTip  * Math.cos(a + step * 0.30), rTip  * Math.sin(a + step * 0.30)]);
      pts.push([rTip  * Math.cos(a + step * 0.52), rTip  * Math.sin(a + step * 0.52)]);
      pts.push([rRoot * Math.cos(a + step * 0.66), rRoot * Math.sin(a + step * 0.66)]);
    }
    return pts;
  }

  /** A gear: toothed rim, web with lightening holes, and a hub. */
  function gear(bld, teeth, rRoot, rTip, depth, m, material) {
    var g = extrudeStar(gearProfile(teeth, rRoot, rTip), depth);
    // extrudeStar builds along Z; stand it up so the axis is Y like everything else
    var toY = M4.mul(m, M4.rotX(Math.PI / 2));
    bld.add(g, mat(material, { m: toY }));
    bld.add(G.tube(rRoot * 0.36, rRoot * 0.16, depth * 1.5, 28),
            mat(material, { m: m, rough: (material.rough || 0.3) + 0.08 }));
    bld.ring(G.cylinder(rRoot * 0.11, rRoot * 0.11, depth * 1.2, 14),
             6, rRoot * 0.62, mat(MAT.iron, { m: m }));
  }

  /** Threaded pin/box connection - a stack of shallow rings reads as thread. */
  function threads(bld, r, y0, count, pitch, material) {
    for (var k = 0; k < count; k++) {
      bld.add(G.torus(r, pitch * 0.30, 30, 8),
              mat(material, { m: M4.trans(0, y0 + k * pitch, 0) }));
    }
  }

  /** Bolt circle around a flange face. */
  function boltCircle(bld, n, radius, y, headR, headH, material) {
    bld.ring(G.cylinder(headR, headR * 0.9, headH, 8),
             n, radius, mat(material, { m: M4.trans(0, y, 0) }));
  }

  /* =====================================================================
     MODEL 01 - Land drilling rig  (homepage hero)
     ===================================================================== */
  function buildRig(scene) {
    var H = 4.5;          // derrick height
    var base = 1.15;      // half-width at the drill floor
    var top = 0.34;       // half-width under the crown

    var stat = new WF.Builder();

    // --- substructure and drill floor -----------------------------------
    stat.add(G.box(3.5, 0.16, 3.5), mat(MAT.iron, { m: M4.trans(0, -1.62, 0) }));
    stat.add(G.box(2.9, 0.9, 2.9), mat(MAT.navyD, { m: M4.trans(0, -1.15, 0) }));
    stat.add(G.box(3.15, 0.14, 3.15), mat(MAT.steelD, { m: M4.trans(0, -0.64, 0) }));

    // Substructure X-bracing on all four sides.
    [0, 1, 2, 3].forEach(function (side) {
      var a = side * Math.PI / 2;
      var c = Math.cos(a), s = Math.sin(a);
      function pt(x, y) { return [x * c - 1.45 * s, y, x * s + 1.45 * c]; }
      strut(stat, pt(-1.3, -1.58), pt(1.3, -0.72), 0.075, MAT.navy);
      strut(stat, pt(1.3, -1.58), pt(-1.3, -0.72), 0.075, MAT.navy);
    });

    // Rotary table.
    stat.add(G.tube(0.52, 0.20, 0.16, 40), mat(MAT.steelD, { m: M4.trans(0, -0.54, 0) }));
    stat.add(G.torus(0.52, 0.045, 44, 10), mat(MAT.gold, { m: M4.trans(0, -0.47, 0) }));
    boltCircle(stat, 12, 0.40, -0.44, 0.035, 0.06, MAT.steelL);

    // --- derrick mast ----------------------------------------------------
    var legs = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
    var bays = 7, k, i;

    function legPoint(idx, t) {                     // t: 0 at floor, 1 at crown
      var w = base + (top - base) * t;
      return [legs[idx][0] * w, -0.56 + H * t, legs[idx][1] * w];
    }

    // Four tapered legs.
    for (i = 0; i < 4; i++) {
      for (k = 0; k < bays; k++) {
        strut(stat, legPoint(i, k / bays), legPoint(i, (k + 1) / bays), 0.062, MAT.navy);
      }
    }

    // Horizontal girts and diagonal bracing on each face of each bay.
    for (k = 0; k <= bays; k++) {
      var t0 = k / bays;
      for (i = 0; i < 4; i++) {
        var j = (i + 1) % 4;
        strut(stat, legPoint(i, t0), legPoint(j, t0), 0.038, MAT.steelD);
        if (k < bays) {
          var t1 = (k + 1) / bays;
          // Alternate the diagonal so the lattice reads as a real K-brace.
          if ((k + i) % 2 === 0) strut(stat, legPoint(i, t0), legPoint(j, t1), 0.032, MAT.steelD);
          else strut(stat, legPoint(j, t0), legPoint(i, t1), 0.032, MAT.steelD);
        }
      }
    }

    // Crown block housing.
    stat.add(G.box(top * 2.5, 0.14, top * 2.5), mat(MAT.steelD, { m: M4.trans(0, H - 0.52, 0) }));
    stat.add(G.box(top * 2.2, 0.34, top * 1.5), mat(MAT.navy, { m: M4.trans(0, H - 0.32, 0) }));
    stat.add(G.box(top * 2.6, 0.10, top * 2.6), mat(MAT.gold, { m: M4.trans(0, H - 0.13, 0) }));

    // Monkey board and stand of pipe racked back.
    stat.add(G.box(0.9, 0.06, 0.34), mat(MAT.gold, { m: M4.trans(0, 1.55, 0.62) }));
    for (i = 0; i < 5; i++) {
      stat.add(G.cylinder(0.045, 0.045, 3.3, 12),
               mat(MAT.steel, { m: M4.trans(-0.34 + i * 0.17, 0.55, 0.66) }));
    }

    // Mud line running up the derrick leg, plus the standpipe.
    stat.add(G.cylinder(0.045, 0.045, 4.0, 14), mat(MAT.paint, { m: M4.trans(-0.95, 1.3, -0.95) }));
    stat.add(G.torus(0.06, 0.02, 20, 8), mat(MAT.gold, { m: M4.trans(-0.95, 3.3, -0.95) }));

    // --- crown sheaves (own part, spins) ---------------------------------
    var sheaves = new WF.Builder();
    for (i = 0; i < 5; i++) {
      sheaves.add(G.torus(0.17, 0.045, 26, 8),
                  mat(MAT.steelL, { m: M4.chain(M4.trans(0, 0, -0.16 + i * 0.08), M4.rotX(Math.PI / 2)) }));
    }
    sheaves.add(G.cylinder(0.045, 0.045, 0.52, 14),
                mat(MAT.gold, { m: M4.rotZ(Math.PI / 2) }));

    // --- travelling block + hook (own part, hoists) ----------------------
    var blk = new WF.Builder();
    blk.add(G.box(0.40, 0.46, 0.30), mat(MAT.navy));
    blk.add(G.box(0.44, 0.07, 0.34), mat(MAT.gold, { m: M4.trans(0, 0.26, 0) }));
    for (i = 0; i < 4; i++) {
      blk.add(G.torus(0.13, 0.038, 22, 8),
              mat(MAT.steelL, { m: M4.chain(M4.trans(0, 0, -0.11 + i * 0.075), M4.rotX(Math.PI / 2)) }));
    }
    blk.add(G.cylinder(0.06, 0.06, 0.34, 14), mat(MAT.steelD, { m: M4.trans(0, -0.38, 0) }));
    blk.add(G.torus(0.14, 0.05, 26, 10), mat(MAT.gold, { m: M4.trans(0, -0.58, 0) }));
    // Drilling line: two taut runs down from the crown.
    blk.add(G.cylinder(0.012, 0.012, 6.0, 6), mat(MAT.steelD, { m: M4.trans(-0.14, 3.1, 0) }));
    blk.add(G.cylinder(0.012, 0.012, 6.0, 6), mat(MAT.steelD, { m: M4.trans(0.14, 3.1, 0) }));

    // --- rotating drill string ------------------------------------------
    var str = new WF.Builder();
    str.add(G.box(0.16, 1.0, 0.16), mat(MAT.gold, { m: M4.trans(0, 0.62, 0) }));     // kelly
    str.add(G.cylinder(0.115, 0.115, 0.30, 26), mat(MAT.steelD, { m: M4.trans(0, 0.08, 0) }));
    str.add(G.cylinder(0.085, 0.085, 2.5, 24), mat(MAT.steel, { m: M4.trans(0, -1.2, 0) }));
    for (i = 0; i < 3; i++) {                                                        // tool joints
      str.add(G.cylinder(0.125, 0.125, 0.16, 24),
              mat(MAT.goldD, { m: M4.trans(0, -0.45 - i * 0.75, 0) }));
    }
    str.add(G.cylinder(0.14, 0.10, 0.22, 24), mat(MAT.steelD, { m: M4.trans(0, -2.5, 0) }));

    scene.addPart(stat);
    scene.addPart(sheaves, function (t) {
      return M4.chain(M4.trans(0, H - 0.32, 0), M4.rotZ(-t * 1.7));
    });
    scene.addPart(blk, function (t) {
      // Slow hoist cycle, easing at the top and bottom of the travel.
      var y = 1.05 + Math.sin(t * 0.42) * 0.85;
      return M4.trans(0, y, 0);
    });
    scene.addPart(str, function (t) { return M4.rotY(t * 1.25); });
  }

  /* =====================================================================
     MODEL 02 - Tricone rock bit
     ===================================================================== */
  function buildTricone(scene) {
    var body = new WF.Builder();

    // API pin connection on top.
    body.add(G.lathe([
      [0.30, 1.55], [0.30, 1.05], [0.34, 0.98], [0.34, 0.98],
      [0.46, 0.86], [0.52, 0.62], [0.60, 0.34]
    ], 40, true, true), MAT.steelD);
    threads(body, 0.305, 1.08, 8, 0.055, MAT.steelL);

    // Bit body and the three welded legs.
    body.add(G.lathe([
      [0.60, 0.34], [0.72, 0.16], [0.76, -0.02], [0.74, -0.20]
    ], 40, false, false), MAT.steelD);

    var legGeo = G.lathe([
      [0.20, 0.34], [0.26, 0.10], [0.27, -0.26], [0.22, -0.52], [0.10, -0.66]
    ], 22, true, true);
    body.ring(legGeo, 3, 0.44, mat(MAT.iron, {}), function () { return M4.rotZ(-0.10); });

    // Jet nozzles between the legs.
    body.ring(G.lathe([[0.10, 0], [0.11, -0.12], [0.075, -0.16], [0.075, -0.24]], 16, true, true),
              3, 0.40, mat(MAT.carbide, { m: M4.chain(M4.rotY(Math.PI / 3), M4.trans(0, -0.14, 0)) }),
              function () { return M4.rotZ(0.22); });

    // Serial-number band, in brand gold.
    body.add(G.torus(0.755, 0.035, 46, 10), mat(MAT.gold, { m: M4.trans(0, 0.06, 0) }));

    scene.addPart(body);

    // --- three rotating cones -------------------------------------------
    for (var c = 0; c < 3; c++) {
      var cone = new WF.Builder();
      cone.add(G.lathe([
        [0.00, 0.62], [0.14, 0.50], [0.26, 0.30], [0.34, 0.04], [0.37, -0.10],
        [0.37, -0.14], [0.30, -0.18], [0.10, -0.20]
      ], 30, false, true), MAT.steelD);

      // Three rows of tungsten-carbide inserts down the cone.
      var rows = [
        { y: 0.42, r: 0.19, n: 8,  s: 0.055 },
        { y: 0.22, r: 0.29, n: 11, s: 0.062 },
        { y: 0.00, r: 0.355, n: 14, s: 0.058 }
      ];
      rows.forEach(function (row) {
        cone.ring(G.stud(row.s, row.s * 1.7, 8), row.n, row.r,
                  mat(MAT.carbide, { m: M4.trans(0, row.y, 0) }),
                  function () { return M4.rotZ(-0.42); });
      });
      cone.add(G.torus(0.365, 0.028, 30, 8), mat(MAT.gold, { m: M4.trans(0, -0.09, 0) }));

      (function (index) {
        scene.addPart(cone, function (t) {
          return M4.chain(
            M4.rotY(index * TAU / 3),
            M4.trans(0.40, -0.30, 0),
            M4.rotZ(-1.15),
            M4.rotY(-t * 2.6)
          );
        });
      })(c);
    }
  }

  /* =====================================================================
     MODEL 03 - PDC drill bit
     ===================================================================== */
  function buildPDC(scene) {
    var b = new WF.Builder();

    b.add(G.lathe([
      [0.28, 1.60], [0.28, 1.10], [0.33, 1.02], [0.33, 1.02], [0.44, 0.90], [0.50, 0.66]
    ], 40, true, true), MAT.steelD);
    threads(b, 0.285, 1.13, 8, 0.055, MAT.steelL);

    b.add(G.lathe([
      [0.50, 0.66], [0.62, 0.44], [0.68, 0.16], [0.68, -0.04],
      [0.60, -0.30], [0.40, -0.46], [0.16, -0.54], [0.00, -0.56]
    ], 44, false, false), MAT.steelD);
    b.add(G.torus(0.683, 0.032, 46, 10), mat(MAT.gold, { m: M4.trans(0, 0.06, 0) }));

    // Six spiral blades. Each is a continuous rib swept from the nose out to
    // the gauge, carrying a row of PDC cutters on its leading edge.
    var blades = 6, bi, s, steps = 14;
    function bladePoint(a0, f) {
      var ang = a0 + f * 0.80;                         // spiral sweep
      var rad = 0.07 + f * 0.615;
      return [Math.cos(ang) * rad, -0.55 + f * f * 0.66, Math.sin(ang) * rad];
    }

    for (bi = 0; bi < blades; bi++) {
      var a0 = bi * TAU / blades;
      for (s = 0; s < steps; s++) {
        var p0 = bladePoint(a0, s / steps);
        var p1 = bladePoint(a0, (s + 1) / steps);
        strut(b, p0, p1, 0.155, MAT.steelL);

        // Cutter pocket, canted forward on the leading face of the rib.
        var f = (s + 0.5) / steps;
        var mid = bladePoint(a0, f);
        var ang2 = a0 + f * 0.80;
        b.add(G.cylinder(0.062, 0.062, 0.075, 16), mat(MAT.carbide, {
          m: M4.chain(
            M4.trans(mid[0], mid[1], mid[2]),
            M4.rotY(-ang2),
            M4.rotZ(Math.PI / 2 - 0.35),
            M4.trans(0, 0.085, 0)
          )
        }));
      }
      // Nozzle in the junk slot behind each blade.
      b.add(G.lathe([[0.075, 0], [0.08, -0.09], [0.05, -0.13], [0.05, -0.19]], 14, true, true),
            mat(MAT.copper, { m: M4.chain(M4.rotY(a0 + 0.55), M4.trans(0.34, -0.14, 0), M4.rotZ(0.30)) }));
    }

    scene.addPart(b, function (t) { return M4.rotY(t * 0.55); });
  }

  /* =====================================================================
     MODEL 04 - Retrievable production packer
     ===================================================================== */
  function buildPacker(scene) {
    var b = new WF.Builder();
    var R = 0.30;                                    // mandrel radius

    // Through-bore mandrel.
    b.add(G.tube(R, R * 0.62, 3.5, 40), MAT.steel);

    // Top sub with a box connection.
    b.add(G.lathe([[R * 0.62, 1.75], [0.40, 1.75], [0.40, 1.44], [0.34, 1.30], [R, 1.30]], 40, false, false),
          MAT.steelD);
    threads(b, 0.375, 1.50, 4, 0.062, MAT.steelL);

    // Upper slips - hardened wickers that bite the casing.
    b.ring(G.lathe([[0.055, -0.24], [0.085, -0.14], [0.09, 0.14], [0.055, 0.24]], 12, true, true),
           8, 0.335, mat(MAT.carbide, { m: M4.trans(0, 0.94, 0) }));
    b.add(G.lathe([[R, 1.20], [0.40, 1.06], [0.40, 0.72], [R, 0.60]], 40, false, false),
          mat(MAT.steelD, {}));

    // Sealing element stack: three elastomer packing elements with steel spacers.
    [0.34, 0.02, -0.30].forEach(function (y) {
      b.add(G.lathe([
        [R, y - 0.15], [0.415, y - 0.09], [0.435, y], [0.415, y + 0.09], [R, y + 0.15]
      ], 40, false, false), MAT.rubber);
    });
    [0.18, -0.14].forEach(function (y) {
      b.add(G.tube(0.375, R, 0.06, 40), mat(MAT.gold, { m: M4.trans(0, y, 0) }));
    });
    b.add(G.tube(0.385, R, 0.07, 40), mat(MAT.goldD, { m: M4.trans(0, 0.52, 0) }));
    b.add(G.tube(0.385, R, 0.07, 40), mat(MAT.goldD, { m: M4.trans(0, -0.48, 0) }));

    // Lower cone and slips.
    b.add(G.lathe([[R, -0.60], [0.40, -0.72], [0.40, -1.06], [R, -1.20]], 40, false, false), MAT.steelD);
    b.ring(G.lathe([[0.055, -0.24], [0.09, -0.14], [0.085, 0.14], [0.055, 0.24]], 12, true, true),
           8, 0.335, mat(MAT.carbide, { m: M4.trans(0, -0.94, 0) }));

    // Hydraulic setting ports.
    b.ring(G.cylinder(0.045, 0.045, 0.09, 12), 4, R,
           mat(MAT.iron, { m: M4.chain(M4.trans(0, 1.12, 0), M4.rotZ(Math.PI / 2)) }));

    // Mill-out extension / bottom shoe.
    b.add(G.lathe([[R, -1.30], [0.33, -1.44], [0.26, -1.66], [R * 0.62, -1.75]], 40, false, false),
          MAT.steelD);

    scene.addPart(b);
  }

  /* =====================================================================
     MODEL 05 - API 5CT casing joint with coupling
     ===================================================================== */
  function buildCasing(scene) {
    var b = new WF.Builder();
    var Ro = 0.42, Ri = 0.345;

    // Two pipe bodies meeting inside one coupling.
    b.add(G.tube(Ro, Ri, 2.0, 46), mat(MAT.steel, { m: M4.trans(0, 1.25, 0) }));
    b.add(G.tube(Ro, Ri, 2.0, 46), mat(MAT.steel, { m: M4.trans(0, -1.25, 0) }));

    // Coupling.
    b.add(G.lathe([
      [Ri, -0.46], [0.50, -0.46], [0.54, -0.38], [0.54, 0.38], [0.50, 0.46], [Ri, 0.46]
    ], 46, false, false), MAT.steelD);

    // Machined pin threads exposed either side of the coupling.
    var k;
    for (k = 0; k < 7; k++) {
      b.add(G.torus(Ro + 0.008, 0.022, 40, 8), mat(MAT.steelL, { m: M4.trans(0, 0.50 + k * 0.058, 0) }));
      b.add(G.torus(Ro + 0.008, 0.022, 40, 8), mat(MAT.steelL, { m: M4.trans(0, -0.50 - k * 0.058, 0) }));
    }

    // Grade stencil bands and the mill's paint ring - how a joint is identified.
    b.add(G.tube(Ro + 0.012, Ro, 0.10, 46), mat(MAT.gold, { m: M4.trans(0, 1.55, 0) }));
    b.add(G.tube(Ro + 0.012, Ro, 0.05, 46), mat(MAT.gold, { m: M4.trans(0, 1.70, 0) }));
    b.add(G.tube(Ro + 0.012, Ro, 0.10, 46), mat(MAT.paint, { m: M4.trans(0, -1.62, 0) }));

    // Thread protector on the far end.
    b.add(G.lathe([[Ri, 2.24], [0.47, 2.24], [0.47, 2.46], [0.30, 2.52], [0.30, 2.52], [Ri, 2.46]],
                  40, false, false), MAT.paint);

    scene.addPart(b, function (t) { return M4.rotY(t * 0.10); });
  }

  /* =====================================================================
     MODEL 06 - Gear train  (plant, machinery, precision components)
     ===================================================================== */
  function buildGears(scene) {
    // Three gears in one vertical plane, centre distances set to the sum of the
    // pitch radii so the teeth genuinely mesh as they turn.
    var specs = [
      { teeth: 24, root: 0.72, tip: 0.88, depth: 0.26, x: -0.78, y:  0.02, spin:  0.85, phase: 0.00, mat: MAT.steel },
      { teeth: 16, root: 0.48, tip: 0.62, depth: 0.26, x:  0.57, y:  0.02, spin: -1.24, phase: 0.19, mat: MAT.steelD },
      { teeth: 12, root: 0.36, tip: 0.48, depth: 0.22, x:  0.90, y:  0.93, spin:  1.62, phase: 0.26, mat: MAT.copper }
    ];

    var frame = new WF.Builder();

    // Open bearing frame rather than a solid backplate, so the gears read as
    // the subject and the page ground shows through the train.
    frame.add(G.box(2.9, 0.14, 0.44), mat(MAT.steelD, { m: M4.trans(-0.10, -1.24, -0.30) }));
    frame.add(G.box(2.9, 0.06, 0.20), mat(MAT.gold, { m: M4.trans(-0.10, -1.34, -0.30) }));

    // Pedestal and bearing boss for every shaft.
    specs.forEach(function (s) {
      var pedH = s.y + 1.24;
      frame.add(G.box(0.22, pedH, 0.22),
                mat(MAT.iron, { m: M4.trans(s.x, -1.24 + pedH / 2, -0.30) }));
      frame.add(G.cylinder(s.root * 0.40, s.root * 0.40, 0.24, 26),
                mat(MAT.iron, { m: M4.chain(M4.trans(s.x, s.y, -0.30), M4.rotX(Math.PI / 2)) }));
      frame.add(G.torus(s.root * 0.40, 0.026, 30, 8),
                mat(MAT.gold, { m: M4.chain(M4.trans(s.x, s.y, -0.19), M4.rotX(Math.PI / 2)) }));
      frame.ring(G.cylinder(0.032, 0.032, 0.07, 8), 6, s.root * 0.40,
                 mat(MAT.steelL, { m: M4.chain(M4.trans(s.x, s.y, -0.20), M4.rotX(Math.PI / 2)) }));
    });
    scene.addPart(frame);

    specs.forEach(function (s, idx) {
      var b = new WF.Builder();
      gear(b, s.teeth, s.root, s.tip, s.depth, M4.ident(), s.mat);
      // Shaft, running along the gear's own axis.
      b.add(G.cylinder(s.root * 0.15, s.root * 0.15, 1.1, 16), mat(MAT.steelL));
      if (idx === 0) {
        // Drive gear gets a gold hub collar so the eye lands on it first.
        b.add(G.torus(s.root * 0.42, 0.035, 34, 8), mat(MAT.gold, { m: M4.trans(0, s.depth * 0.62, 0) }));
      }
      scene.addPart(b, function (t) {
        return M4.chain(
          M4.trans(s.x, s.y, 0),
          M4.rotX(Math.PI / 2),                    // stand the gear up, axis toward the viewer
          M4.rotY(s.phase + t * s.spin)
        );
      });
    });
  }

  /* =====================================================================
     MODEL 07 - Positive displacement mud motor  (drilling fluids)
     ===================================================================== */
  function buildMudMotor(scene) {
    var b = new WF.Builder();
    var R = 0.34;

    // Top sub and dump valve.
    b.add(G.lathe([[0.20, 2.10], [0.36, 2.10], [0.36, 1.86], [R, 1.72]], 40, true, false), MAT.steelD);
    threads(b, 0.335, 1.90, 3, 0.058, MAT.steelL);

    // Power section housing.
    b.add(G.cylinder(R, R, 1.9, 44), mat(MAT.steel, { m: M4.trans(0, 0.78, 0) }));
    b.add(G.torus(R + 0.012, 0.028, 44, 8), mat(MAT.gold, { m: M4.trans(0, 1.52, 0) }));
    b.add(G.torus(R + 0.012, 0.028, 44, 8), mat(MAT.gold, { m: M4.trans(0, 0.05, 0) }));

    // Bent housing and adjustable ring.
    b.add(G.cylinder(0.32, 0.32, 0.34, 40), mat(MAT.steelD, { m: M4.trans(0, -0.32, 0) }));
    b.add(G.torus(0.335, 0.045, 40, 10), mat(MAT.goldD, { m: M4.trans(0, -0.32, 0) }));

    // Bearing pack and bit box.
    b.add(G.cylinder(0.31, 0.31, 0.95, 40), mat(MAT.steel, { m: M4.trans(0, -0.98, 0) }));
    b.ring(G.box(0.06, 0.55, 0.10), 6, 0.315, mat(MAT.iron, { m: M4.trans(0, -0.98, 0) }));
    b.add(G.lathe([[0.31, -1.46], [0.36, -1.56], [0.36, -1.84], [0.22, -1.94]], 40, false, true),
          MAT.steelD);
    scene.addPart(b);

    // Helical rotor turning inside the (cut-away) stator.
    var rotor = new WF.Builder();
    var lobes = 4, turns = 2.4, steps = 90, k;
    for (k = 0; k <= steps; k++) {
      var f = k / steps;
      var a = f * turns * TAU;
      var y = -0.92 + f * 1.84;
      var off = 0.088;
      rotor.add(G.sphere(0.135, 14, 10),
                mat(MAT.copper, { m: M4.trans(Math.cos(a) * off, y, Math.sin(a) * off) }));
      if (k % 6 === 0) {
        rotor.add(G.torus(0.175, 0.022, 20, 6),
                  mat(MAT.gold, { m: M4.trans(0, y, 0) }));
      }
    }
    scene.addPart(rotor, function (t) {
      // The rotor nutates: it spins about its own axis while orbiting the bore.
      return M4.chain(M4.trans(0, 0.78, 0), M4.rotY(t * 1.9));
    });

    void lobes;
  }

  /* =====================================================================
     MODEL 08 - Subsea christmas tree
     ===================================================================== */
  function buildTree(scene) {
    var b = new WF.Builder();

    // Guide frame.
    var fw = 1.25, fh = 1.45;
    var corners = [[-1, -1], [1, -1], [1, 1], [-1, 1]];
    corners.forEach(function (c, i) {
      var a = [c[0] * fw, -fh, c[1] * fw], t = [c[0] * fw * 0.82, fh * 0.35, c[1] * fw * 0.82];
      strut(b, a, t, 0.085, MAT.paint);
      var n = corners[(i + 1) % 4];
      strut(b, a, [n[0] * fw, -fh, n[1] * fw], 0.07, MAT.paint);
      strut(b, t, [n[0] * fw * 0.82, fh * 0.35, n[1] * fw * 0.82], 0.07, MAT.paint);
    });
    // Guide funnels on the frame corners.
    b.ring(G.lathe([[0.20, 0], [0.13, 0.20], [0.13, 0.30]], 20, false, false), 4, fw * 1.0,
           mat(MAT.gold, { m: M4.trans(0, fh * 0.35, 0) }), function () { return M4.rotY(Math.PI / 4); });

    // Tree body over the tubing head.
    b.add(G.box(0.86, 1.40, 0.86), mat(MAT.steelD, { m: M4.trans(0, -0.35, 0) }));
    b.add(G.lathe([[0.44, 0.35], [0.44, 0.48], [0.52, 0.56], [0.52, 0.70], [0.34, 0.80]],
                  36, false, true), MAT.steelD);
    boltCircle(b, 12, 0.46, 0.52, 0.045, 0.09, MAT.steelL);

    // Production and annulus wing valves with their hydraulic actuators.
    var valves = [
      { a: 0,           y:  0.16, r: 0.62 },
      { a: Math.PI,     y:  0.16, r: 0.62 },
      { a: Math.PI / 2, y: -0.42, r: 0.62 }
    ];
    valves.forEach(function (v) {
      var base = M4.chain(M4.rotY(v.a), M4.trans(v.r, v.y, 0));
      b.add(G.cylinder(0.17, 0.17, 0.60, 26),
            mat(MAT.steelD, { m: M4.mul(base, M4.rotZ(Math.PI / 2)) }));
      b.add(G.cylinder(0.24, 0.24, 0.34, 26),
            mat(MAT.gold, { m: M4.chain(base, M4.trans(0.34, 0, 0), M4.rotZ(Math.PI / 2)) }));
      b.add(G.torus(0.245, 0.03, 26, 8),
            mat(MAT.steelL, { m: M4.chain(base, M4.trans(0.34, 0, 0), M4.rotZ(Math.PI / 2)) }));
    });

    // Flowline jumper connector and the ROV panel.
    b.add(G.cylinder(0.13, 0.13, 0.7, 22),
          mat(MAT.steel, { m: M4.chain(M4.trans(0.62, -0.95, 0.30), M4.rotZ(Math.PI / 2)) }));
    b.add(G.box(0.44, 0.34, 0.06), mat(MAT.gold, { m: M4.trans(-0.30, -0.55, 0.46) }));
    b.ring(G.cylinder(0.035, 0.035, 0.07, 10), 4, 0.12,
           mat(MAT.steelL, { m: M4.chain(M4.trans(-0.30, -0.55, 0.50), M4.rotX(Math.PI / 2)) }));

    // Mudmat.
    b.add(G.box(2.9, 0.08, 2.9), mat(MAT.navyD, { m: M4.trans(0, -1.50, 0) }));
    b.add(G.box(3.0, 0.05, 3.0), mat(MAT.gold, { m: M4.trans(0, -1.56, 0) }));

    scene.addPart(b);
  }

  /* =====================================================================
     MODEL 09 - Flanged gate valve  (services)
     ===================================================================== */
  function buildValve(scene) {
    var b = new WF.Builder();

    // Raised-face flanges either side of the body.
    function flange(x) {
      var m = M4.chain(M4.trans(x, 0, 0), M4.rotZ(Math.PI / 2));
      b.add(G.lathe([[0.20, -0.10], [0.62, -0.10], [0.62, 0.06], [0.42, 0.06], [0.42, 0.13], [0.20, 0.13]],
                    40, false, false), mat(MAT.steelD, { m: m }));
      b.ring(G.cylinder(0.055, 0.055, 0.30, 8), 8, 0.52,
             mat(MAT.steelL, { m: M4.chain(m, M4.trans(0, 0.02, 0)) }));
      b.add(G.cylinder(0.20, 0.20, 0.55, 30), mat(MAT.steel, { m: m }));
    }
    flange(-0.95);
    flange(0.95);

    // Body and bonnet.
    b.add(G.lathe([[0.20, -0.55], [0.46, -0.44], [0.50, 0.05], [0.44, 0.30]], 36, true, false),
          MAT.paint);
    b.add(G.cylinder(0.20, 0.20, 1.30, 30), mat(MAT.steel, { m: M4.rotZ(Math.PI / 2) }));
    b.add(G.lathe([[0.44, 0.30], [0.48, 0.38], [0.48, 0.50], [0.30, 0.58], [0.30, 0.58], [0.22, 0.62]],
                  36, false, true), MAT.steelD);
    boltCircle(b, 8, 0.40, 0.44, 0.045, 0.14, MAT.steelL);

    // Rising stem.
    b.add(G.cylinder(0.055, 0.055, 0.85, 18), mat(MAT.steelL, { m: M4.trans(0, 0.95, 0) }));
    threads(b, 0.062, 0.72, 9, 0.052, MAT.steelL);

    scene.addPart(b);

    // Handwheel - turns, as if the valve is being stroked.
    var hw = new WF.Builder();
    hw.add(G.torus(0.46, 0.045, 44, 10), mat(MAT.gold));
    hw.ring(G.box(0.045, 0.045, 0.86), 5, 0, mat(MAT.gold), function (k) {
      return M4.rotY(k * Math.PI / 5);
    });
    hw.add(G.cylinder(0.10, 0.10, 0.14, 20), mat(MAT.steelD));
    scene.addPart(hw, function (t) {
      return M4.chain(M4.trans(0, 1.40, 0), M4.rotY(Math.sin(t * 0.6) * 1.4));
    });
  }

  /* =====================================================================
     Registry - camera framing per model
     ===================================================================== */
  var MODELS = {
    rig:      { build: buildRig,      camera: [0, 2.1, 15.0], target: [0, 1.35, 0], fov: 34, autoSpin: 0.14, maxPitch: 0.42 },
    tricone:  { build: buildTricone,  camera: [0, 0.9, 5.2],  target: [0, 0.25, 0], fov: 32, autoSpin: 0.30 },
    pdc:      { build: buildPDC,      camera: [0, 0.8, 5.0],  target: [0, 0.20, 0], fov: 32, autoSpin: 0.28 },
    packer:   { build: buildPacker,   camera: [0, 0.2, 8.2],  target: [0, 0.05, 0], fov: 32, autoSpin: 0.26 },
    casing:   { build: buildCasing,   camera: [0, 0.5, 9.6],  target: [0, 0.30, 0], fov: 32, autoSpin: 0.24 },
    gears:    { build: buildGears,    camera: [0, 0.5, 7.6],  target: [0, 0.15, 0], fov: 34, autoSpin: 0.16, maxPitch: 0.40 },
    mudmotor: { build: buildMudMotor, camera: [0, 0.3, 8.8],  target: [0, 0.10, 0], fov: 32, autoSpin: 0.26 },
    tree:     { build: buildTree,     camera: [0, 1.0, 8.4],  target: [0, -0.2, 0], fov: 34, autoSpin: 0.24 },
    valve:    { build: buildValve,    camera: [0, 1.0, 7.4],  target: [0, 0.45, 0], fov: 32, autoSpin: 0.26 }
  };

  /**
   * Mount a model on a canvas. Returns the running Scene, or null if the
   * name is unknown or WebGL is not available.
   */
  function mount(canvas, name, overrides) {
    var spec = MODELS[name];
    if (!spec || !WF.supported) return null;

    var opts = {
      camera: spec.camera, target: spec.target, fov: spec.fov,
      autoSpin: spec.autoSpin, maxPitch: spec.maxPitch,
      pitch: spec.pitch || 0, yaw: spec.yaw || 0
    }, k;
    if (overrides) for (k in overrides) if (overrides.hasOwnProperty(k)) opts[k] = overrides[k];

    var scene = new WF.Scene(canvas, opts);
    spec.build(scene);
    return scene.start();
  }

  global.WFScenes = { models: MODELS, mount: mount, MAT: MAT };
})(window);
