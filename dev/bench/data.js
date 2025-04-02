window.BENCHMARK_DATA = {
  "lastUpdate": 1743574648297,
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
      },
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
          "id": "a5297a163d9e22f4f6acd1109ec2ce5c2e52bbf4",
          "message": "change method of ignoring benchmark tests since pytest-benchmark isn't installed for normal workflows",
          "timestamp": "2025-04-01T22:39:46-07:00",
          "tree_id": "ef31541e4c98141168fa97a8637115ab183d04e9",
          "url": "https://github.com/iausathub/satchecker/commit/a5297a163d9e22f4f6acd1109ec2ce5c2e52bbf4"
        },
        "date": 1743572469561,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139632.36499543206,
            "unit": "iter/sec",
            "range": "stddev: 8.869045407759612e-7",
            "extra": "mean: 7.161663415446084 usec\nrounds: 12098"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 189512.10278260455,
            "unit": "iter/sec",
            "range": "stddev: 8.581189580147822e-7",
            "extra": "mean: 5.276707847768078 usec\nrounds: 74047"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 748117.4767282299,
            "unit": "iter/sec",
            "range": "stddev: 4.0013609155468184e-7",
            "extra": "mean: 1.3366884628512323 usec\nrounds: 68743"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 690387.6242595242,
            "unit": "iter/sec",
            "range": "stddev: 4.3983552186807854e-7",
            "extra": "mean: 1.448461653802892 usec\nrounds: 86723"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 360.972129243353,
            "unit": "iter/sec",
            "range": "stddev: 0.0002735284830882661",
            "extra": "mean: 2.7702969813656715 msec\nrounds: 322"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 232.54885921270292,
            "unit": "iter/sec",
            "range": "stddev: 0.00016022139703108666",
            "extra": "mean: 4.300171600004887 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 106037.24751388251,
            "unit": "iter/sec",
            "range": "stddev: 0.000003428840291844077",
            "extra": "mean: 9.430648413135007 usec\nrounds: 26497"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152032.53822804222,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011018287875548596",
            "extra": "mean: 6.577539332402931 usec\nrounds: 49908"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12048372.344208712,
            "unit": "iter/sec",
            "range": "stddev: 1.1971789827378046e-8",
            "extra": "mean: 82.99876293924554 nsec\nrounds: 118822"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3667.878391050989,
            "unit": "iter/sec",
            "range": "stddev: 0.00005072379476690727",
            "extra": "mean: 272.637174242154 usec\nrounds: 1188"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 149.80786284902155,
            "unit": "iter/sec",
            "range": "stddev: 0.0003459118559703309",
            "extra": "mean: 6.675217047904982 msec\nrounds: 167"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 153579.57526577197,
            "unit": "iter/sec",
            "range": "stddev: 0.000001764648662683359",
            "extra": "mean: 6.511282494885688 usec\nrounds: 10694"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16595.986541766935,
            "unit": "iter/sec",
            "range": "stddev: 0.000005552867390489228",
            "extra": "mean: 60.25553211213513 usec\nrounds: 9716"
          }
        ]
      },
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
          "id": "3e7b2d38f5f6dea2c8bb0f4bc446a6bf31847f70",
          "message": "Add random time benchmark for visualization testing",
          "timestamp": "2025-04-01T23:16:02-07:00",
          "tree_id": "baba15db68ee5dd63cbae9df09dc57353435a6f5",
          "url": "https://github.com/iausathub/satchecker/commit/3e7b2d38f5f6dea2c8bb0f4bc446a6bf31847f70"
        },
        "date": 1743574647978,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 140384.84816527533,
            "unit": "iter/sec",
            "range": "stddev: 9.053261378280841e-7",
            "extra": "mean: 7.123275859676097 usec\nrounds: 13931"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 189146.94876795233,
            "unit": "iter/sec",
            "range": "stddev: 7.342529953397566e-7",
            "extra": "mean: 5.286894694911583 usec\nrounds: 70443"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 749950.3963914359,
            "unit": "iter/sec",
            "range": "stddev: 4.376387675488066e-7",
            "extra": "mean: 1.333421523359061 usec\nrounds: 27951"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 691197.2470848705,
            "unit": "iter/sec",
            "range": "stddev: 4.31486655958291e-7",
            "extra": "mean: 1.4467650214428769 usec\nrounds: 75109"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 332.18254535401206,
            "unit": "iter/sec",
            "range": "stddev: 0.004116884065336686",
            "extra": "mean: 3.0103929721361022 msec\nrounds: 323"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 217.96608090332336,
            "unit": "iter/sec",
            "range": "stddev: 0.0007268481580693489",
            "extra": "mean: 4.587869799996724 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 106325.47743943332,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029802651501548343",
            "extra": "mean: 9.405083561177843 usec\nrounds: 27429"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152175.1434474732,
            "unit": "iter/sec",
            "range": "stddev: 0.000001006588487369754",
            "extra": "mean: 6.571375438493826 usec\nrounds: 49883"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11849229.973058878,
            "unit": "iter/sec",
            "range": "stddev: 8.771226062679845e-9",
            "extra": "mean: 84.39366965388592 nsec\nrounds: 117289"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3691.853082322283,
            "unit": "iter/sec",
            "range": "stddev: 0.0000477941786493559",
            "extra": "mean: 270.86668339764236 usec\nrounds: 1295"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 150.3675916490095,
            "unit": "iter/sec",
            "range": "stddev: 0.0003193069057469437",
            "extra": "mean: 6.650369198797946 msec\nrounds: 166"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157177.2820508536,
            "unit": "iter/sec",
            "range": "stddev: 0.000001928493112012591",
            "extra": "mean: 6.362242602442108 usec\nrounds: 10882"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 17238.40772754932,
            "unit": "iter/sec",
            "range": "stddev: 0.000005871153496178573",
            "extra": "mean: 58.00999812771942 usec\nrounds: 9614"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.00625292937044,
            "unit": "iter/sec",
            "range": "stddev: 0.022558415448457592",
            "extra": "mean: 58.801900933330366 msec\nrounds: 15"
          }
        ]
      }
    ]
  }
}