$fn = 50;


difference() {
	union() {
		hull() {
			translate(v = [-32.0000000000, 32.0000000000, 0]) {
				cylinder(h = 12, r = 5);
			}
			translate(v = [32.0000000000, 32.0000000000, 0]) {
				cylinder(h = 12, r = 5);
			}
			translate(v = [-32.0000000000, -32.0000000000, 0]) {
				cylinder(h = 12, r = 5);
			}
			translate(v = [32.0000000000, -32.0000000000, 0]) {
				cylinder(h = 12, r = 5);
			}
		}
		translate(v = [105, 0, 0]) {
			hull() {
				translate(v = [-32.0000000000, 32.0000000000, 0]) {
					cylinder(h = 12, r = 5);
				}
				translate(v = [32.0000000000, 32.0000000000, 0]) {
					cylinder(h = 12, r = 5);
				}
				translate(v = [-32.0000000000, -32.0000000000, 0]) {
					cylinder(h = 12, r = 5);
				}
				translate(v = [32.0000000000, -32.0000000000, 0]) {
					cylinder(h = 12, r = 5);
				}
			}
		}
	}
	union() {
		translate(v = [105, -37.0000000000, 6.0000000000]) {
			rotate(a = [90, 0, 0]) {
				difference() {
					union() {
						#translate(v = [0, 0, -74.0000000000]) {
							cylinder(h = 74, r = 2.2500000000);
						}
						#translate(v = [0, 0, -4.2000000000]) {
							cylinder(h = 4.2000000000, r1 = 2.7500000000, r2 = 5.5000000000);
						}
						#cylinder(h = 250, r = 5.5000000000);
						#translate(v = [0, 0, -74.0000000000]) {
							cylinder(h = 74, r = 2.7500000000);
						}
						#translate(v = [0, 0, -74.0000000000]) {
							cylinder(h = 74, r = 2.2500000000);
						}
					}
					union();
				}
			}
		}
		translate(v = [0, -37.0000000000, 6.0000000000]) {
			rotate(a = [90, 0, 0]) {
				difference() {
					union() {
						#translate(v = [0, 0, -74.0000000000]) {
							cylinder(h = 74, r = 2.2500000000);
						}
						#translate(v = [0, 0, -4.2000000000]) {
							cylinder(h = 4.2000000000, r1 = 2.7500000000, r2 = 5.5000000000);
						}
						#cylinder(h = 250, r = 5.5000000000);
						#translate(v = [0, 0, -74.0000000000]) {
							cylinder(h = 74, r = 2.7500000000);
						}
						#translate(v = [0, 0, -74.0000000000]) {
							cylinder(h = 74, r = 2.2500000000);
						}
					}
					union();
				}
			}
		}
		#translate(v = [18, 18, 0.0000000000]) {
			cylinder(h = 12, r = 15.0000000000);
		}
		#translate(v = [-18, 18, 0.0000000000]) {
			cylinder(h = 12, r = 15.0000000000);
		}
		#translate(v = [18, -18, 0.0000000000]) {
			cylinder(h = 12, r = 15.0000000000);
		}
		#translate(v = [-18, -18, 0.0000000000]) {
			cylinder(h = 12, r = 15.0000000000);
		}
	}
}