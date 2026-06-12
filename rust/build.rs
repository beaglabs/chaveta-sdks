fn main() {
    prost_build::Config::new()
        .out_dir("src/gen")
        .compile_protos(
            &["types.proto", "event.proto", "analytics.proto"],
            &["../../packages/schemas/proto/robolytics"],
        )
        .unwrap();
}
