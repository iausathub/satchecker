window.BENCHMARK_DATA = {
  "lastUpdate": 1743572220774,
  "repoUrl": "https://github.com/iausathub/satchecker",
  "entries": {
    "Benchmark": [
      {
        "commit": {
          "author": {
            "email": "michelle.dadighat@noirlab.edu",
            "name": "Michelle Dadighat",
            "username": "mdadighat"
          },
          "committer": {
            "email": "michelle.dadighat@noirlab.edu",
            "name": "Michelle Dadighat",
            "username": "mdadighat"
          },
          "distinct": true,
          "id": "781cf6a8ec5c1766a39880ecf3b8cec31e5dc788",
          "message": "Add supporting services, skip benchmark tests in other workflows",
          "timestamp": "2025-04-01T22:35:30-07:00",
          "tree_id": "c07f09cf4a615e67e60f7289b76cc2a9f8f879a0",
          "url": "https://github.com/iausathub/satchecker/commit/781cf6a8ec5c1766a39880ecf3b8cec31e5dc788"
        },
        "date": 1743572220202,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138286.70882232438,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012371378239857366",
            "extra": "mean: 7.231352951532277 usec\nrounds: 11299"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187465.9362026896,
            "unit": "iter/sec",
            "range": "stddev: 7.542138401935421e-7",
            "extra": "mean: 5.334302435183704 usec\nrounds: 55149"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 763756.5731491876,
            "unit": "iter/sec",
            "range": "stddev: 4.045421196686887e-7",
            "extra": "mean: 1.3093177003724012 usec\nrounds: 50513"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 693074.0259949232,
            "unit": "iter/sec",
            "range": "stddev: 5.33483539926314e-7",
            "extra": "mean: 1.4428473186027677 usec\nrounds: 47419"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 357.1869338215311,
            "unit": "iter/sec",
            "range": "stddev: 0.00041814035738066337",
            "extra": "mean: 2.7996544814812605 msec\nrounds: 297"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 229.33457014969298,
            "unit": "iter/sec",
            "range": "stddev: 0.00012888667667658208",
            "extra": "mean: 4.3604416000050605 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 96884.00126012256,
            "unit": "iter/sec",
            "range": "stddev: 0.000003683185847668351",
            "extra": "mean: 10.321621598958464 usec\nrounds: 15658"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152399.4208738172,
            "unit": "iter/sec",
            "range": "stddev: 0.000001043455396927977",
            "extra": "mean: 6.561704724770406 usec\nrounds: 17228"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11891547.609824069,
            "unit": "iter/sec",
            "range": "stddev: 8.578764919063886e-9",
            "extra": "mean: 84.09334367659372 nsec\nrounds: 118274"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3446.5156625544255,
            "unit": "iter/sec",
            "range": "stddev: 0.00006321039428958263",
            "extra": "mean: 290.14810838226055 usec\nrounds: 1181"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.53100961303372,
            "unit": "iter/sec",
            "range": "stddev: 0.0003795663411869029",
            "extra": "mean: 6.732600839415888 msec\nrounds: 137"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 155164.30675079,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016260044797891194",
            "extra": "mean: 6.444781154509354 usec\nrounds: 10464"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16859.399145625383,
            "unit": "iter/sec",
            "range": "stddev: 0.000005733136647414408",
            "extra": "mean: 59.31409484776784 usec\nrounds: 8656"
          }
        ]
      }
    ]
  }
}