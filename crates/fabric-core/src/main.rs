//! `fabric-core` binary — resolve the stable-state kernel and report validity.
//! Exit 0 iff the graph resolves at node + box (real + stable).

use fabric_core::kernel;

fn main() {
    let g = kernel();
    let r = g.resolve();
    println!("fabric-core :: boxes={}", g.boxes.len());
    println!("  NODE  real   : {}", r.node_real);
    println!("  BOX   stable : {}", r.box_stable);
    println!(
        "  RESULT       : {}",
        if r.valid { "VALID (real + stable)" } else { "INVALID" }
    );
    if !r.valid {
        for d in &r.dangling {
            eprintln!("  dangling: {d}");
        }
        for u in &r.unstable {
            eprintln!("  unstable: {u}");
        }
    }
    std::process::exit(if r.valid { 0 } else { 1 });
}
