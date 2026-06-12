mod gen {
    include!(concat!(env!("OUT_DIR"), "/gen/robolytics.v1.rs"));
}

pub use gen::*;
