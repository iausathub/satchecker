window.BENCHMARK_DATA = {
  "lastUpdate": 1743641302074,
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
      },
      {
        "commit": {
          "author": {
            "email": "michelle.dadighat@noirlab.edu",
            "name": "Michelle Dadighat",
            "username": "mdadighat"
          },
          "committer": {
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "1b6491d51e23aa4b9bcb7490ce91cb63ef78c72c",
          "message": "Update benchmark.yml",
          "timestamp": "2025-04-02T12:28:53-07:00",
          "tree_id": "af04ec563026f5ebbd3d70148aac1c1775f58b6d",
          "url": "https://github.com/iausathub/satchecker/commit/1b6491d51e23aa4b9bcb7490ce91cb63ef78c72c"
        },
        "date": 1743622219281,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 121739.20133632697,
            "unit": "iter/sec",
            "range": "stddev: 0.000002917752692402527",
            "extra": "mean: 8.21428093024297 usec\nrounds: 11138"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 164977.9184495814,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020855010322421313",
            "extra": "mean: 6.0614172453970445 usec\nrounds: 39895"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 747335.3257742708,
            "unit": "iter/sec",
            "range": "stddev: 3.9717218248004674e-7",
            "extra": "mean: 1.3380874227562545 usec\nrounds: 42243"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 690807.06040884,
            "unit": "iter/sec",
            "range": "stddev: 4.957119223745188e-7",
            "extra": "mean: 1.4475821938012192 usec\nrounds: 39267"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 325.11073755453094,
            "unit": "iter/sec",
            "range": "stddev: 0.004551329587034037",
            "extra": "mean: 3.075875031141565 msec\nrounds: 289"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 219.48225453046814,
            "unit": "iter/sec",
            "range": "stddev: 0.00040687614631609663",
            "extra": "mean: 4.556177000000616 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 105155.44700966508,
            "unit": "iter/sec",
            "range": "stddev: 0.000002935724122850136",
            "extra": "mean: 9.50973086451801 usec\nrounds: 26247"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152369.9499057218,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010934914753553626",
            "extra": "mean: 6.562973871283317 usec\nrounds: 38272"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12182627.136780513,
            "unit": "iter/sec",
            "range": "stddev: 8.046990711360288e-9",
            "extra": "mean: 82.08410130043279 nsec\nrounds: 121125"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3646.96632273105,
            "unit": "iter/sec",
            "range": "stddev: 0.0000502996205148521",
            "extra": "mean: 274.2005029679421 usec\nrounds: 1179"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 149.38823221712116,
            "unit": "iter/sec",
            "range": "stddev: 0.00033117691999708185",
            "extra": "mean: 6.6939676918232625 msec\nrounds: 159"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156938.82220507192,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016840484435387025",
            "extra": "mean: 6.371909677602271 usec\nrounds: 10540"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 17006.5904042247,
            "unit": "iter/sec",
            "range": "stddev: 0.000006042778675790822",
            "extra": "mean: 58.80073408198181 usec\nrounds: 8371"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.279921810452766,
            "unit": "iter/sec",
            "range": "stddev: 0.027995295639197445",
            "extra": "mean: 54.70482917646744 msec\nrounds: 17"
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
          "id": "32771016d5d9984e9c576ef02e96112e7b8b484a",
          "message": "Merge commit 'ede3237740552286f40b00b9b53fec12497d11fa' into develop",
          "timestamp": "2025-04-02T14:37:35-07:00",
          "tree_id": "4c8f289a14141fb205a6a6c02bd6fb7f68a02c75",
          "url": "https://github.com/iausathub/satchecker/commit/32771016d5d9984e9c576ef02e96112e7b8b484a"
        },
        "date": 1743629959440,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 137712.0420368044,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010545116132356375",
            "extra": "mean: 7.261529095129848 usec\nrounds: 10964"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187368.04971928173,
            "unit": "iter/sec",
            "range": "stddev: 7.786811579160644e-7",
            "extra": "mean: 5.337089228917196 usec\nrounds: 59734"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 750453.1153806015,
            "unit": "iter/sec",
            "range": "stddev: 4.110719520546286e-7",
            "extra": "mean: 1.3325282812542363 usec\nrounds: 46621"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 689638.2910412514,
            "unit": "iter/sec",
            "range": "stddev: 4.5361940990042597e-7",
            "extra": "mean: 1.4500354939545896 usec\nrounds: 59165"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 324.27337028557514,
            "unit": "iter/sec",
            "range": "stddev: 0.004737818341931881",
            "extra": "mean: 3.083817826666859 msec\nrounds: 300"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 215.98503517424217,
            "unit": "iter/sec",
            "range": "stddev: 0.0007337626624299101",
            "extra": "mean: 4.629950400004645 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 103831.10588430247,
            "unit": "iter/sec",
            "range": "stddev: 0.000007686242433322853",
            "extra": "mean: 9.631025225853664 usec\nrounds: 24023"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152755.31447420028,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011300046275913579",
            "extra": "mean: 6.546417081736922 usec\nrounds: 36940"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11084704.197176205,
            "unit": "iter/sec",
            "range": "stddev: 2.3497158439352654e-8",
            "extra": "mean: 90.21440556388886 nsec\nrounds: 116741"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3498.72152827266,
            "unit": "iter/sec",
            "range": "stddev: 0.00006030283386572701",
            "extra": "mean: 285.81868888939727 usec\nrounds: 1125"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 147.2484430450825,
            "unit": "iter/sec",
            "range": "stddev: 0.0006169163264378593",
            "extra": "mean: 6.79124328461547 msec\nrounds: 130"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156979.8210553458,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017215861859734521",
            "extra": "mean: 6.370245508481207 usec\nrounds: 10631"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16433.35902901483,
            "unit": "iter/sec",
            "range": "stddev: 0.000005928232636880461",
            "extra": "mean: 60.8518318278323 usec\nrounds: 7528"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.096057555228153,
            "unit": "iter/sec",
            "range": "stddev: 0.019713958678986686",
            "extra": "mean: 55.260655363636864 msec\nrounds: 11"
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
            "email": "noreply@github.com",
            "name": "GitHub",
            "username": "web-flow"
          },
          "distinct": true,
          "id": "bd7306cc2df8e7e2e96871b5cf8d6f14c8a315eb",
          "message": "Merge pull request #134 from iausathub/develop\n\nTesting workflow updates",
          "timestamp": "2025-04-02T16:48:07-07:00",
          "tree_id": "1ede51d897e09c5b36430cb3997f92101da075c7",
          "url": "https://github.com/iausathub/satchecker/commit/bd7306cc2df8e7e2e96871b5cf8d6f14c8a315eb"
        },
        "date": 1743637781481,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139742.36809266597,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010625645200621382",
            "extra": "mean: 7.156025861368542 usec\nrounds: 9899"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186207.80186233262,
            "unit": "iter/sec",
            "range": "stddev: 8.283265158517789e-7",
            "extra": "mean: 5.370344260544578 usec\nrounds: 54482"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 773352.3036400145,
            "unit": "iter/sec",
            "range": "stddev: 4.141206087925354e-7",
            "extra": "mean: 1.2930717284906246 usec\nrounds: 61691"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 705311.0306277853,
            "unit": "iter/sec",
            "range": "stddev: 4.376058887451262e-7",
            "extra": "mean: 1.4178142075984792 usec\nrounds: 59841"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 318.2019833714484,
            "unit": "iter/sec",
            "range": "stddev: 0.0047457469587967056",
            "extra": "mean: 3.1426579727903983 msec\nrounds: 294"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.71571665771205,
            "unit": "iter/sec",
            "range": "stddev: 0.0004887691017812394",
            "extra": "mean: 4.61433999998917 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 91182.99334991198,
            "unit": "iter/sec",
            "range": "stddev: 0.0000051145645261876275",
            "extra": "mean: 10.966957359718718 usec\nrounds: 13649"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 144590.39951972276,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016895187179865119",
            "extra": "mean: 6.916088504642355 usec\nrounds: 35196"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11983520.73793075,
            "unit": "iter/sec",
            "range": "stddev: 9.996281769997512e-9",
            "extra": "mean: 83.44793002565892 nsec\nrounds: 64025"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3444.261407508015,
            "unit": "iter/sec",
            "range": "stddev: 0.00005902800914618345",
            "extra": "mean: 290.33800913604813 usec\nrounds: 1204"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 140.0035343948985,
            "unit": "iter/sec",
            "range": "stddev: 0.000780221408145747",
            "extra": "mean: 7.142676821139156 msec\nrounds: 123"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156794.36938180414,
            "unit": "iter/sec",
            "range": "stddev: 0.00000519048340093815",
            "extra": "mean: 6.377780043650275 usec\nrounds: 10593"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16740.459051324087,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061093104734655305",
            "extra": "mean: 59.73551841882764 usec\nrounds: 8198"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 19.948034737819377,
            "unit": "iter/sec",
            "range": "stddev: 0.028842199936114185",
            "extra": "mean: 50.13025158333543 msec\nrounds: 12"
          }
        ]
      },
      {
        "commit": {
          "author": {
            "name": "Michelle Dadighat",
            "username": "mdadighat",
            "email": "michelle.dadighat@noirlab.edu"
          },
          "committer": {
            "name": "Michelle Dadighat",
            "username": "mdadighat",
            "email": "michelle.dadighat@noirlab.edu"
          },
          "id": "094372e99afc054a306ba968058cd0d86b7b5fc4",
          "message": "Disable new workflows from running on push for now, test/draft version of a dashboard using new actions' results",
          "timestamp": "2025-04-02T22:39:05Z",
          "url": "https://github.com/iausathub/satchecker/commit/094372e99afc054a306ba968058cd0d86b7b5fc4"
        },
        "date": 1743641301337,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 141062.54999431217,
            "unit": "iter/sec",
            "range": "stddev: 8.938621649246548e-7",
            "extra": "mean: 7.08905375693493 usec\nrounds: 11924"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 192775.03137163943,
            "unit": "iter/sec",
            "range": "stddev: 8.174622717649713e-7",
            "extra": "mean: 5.187393786865271 usec\nrounds: 24465"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 726778.4445285449,
            "unit": "iter/sec",
            "range": "stddev: 5.427947584496136e-7",
            "extra": "mean: 1.3759351388698542 usec\nrounds: 63212"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 641671.0006287061,
            "unit": "iter/sec",
            "range": "stddev: 6.091240145458628e-7",
            "extra": "mean: 1.5584310324452952 usec\nrounds: 60021"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 336.8339980395374,
            "unit": "iter/sec",
            "range": "stddev: 0.0038025582099855495",
            "extra": "mean: 2.9688214545451572 msec\nrounds: 330"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 231.28977866177976,
            "unit": "iter/sec",
            "range": "stddev: 0.00011506226324802667",
            "extra": "mean: 4.323580599998422 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 107080.8944408106,
            "unit": "iter/sec",
            "range": "stddev: 0.000014228716391942904",
            "extra": "mean: 9.338734096517602 usec\nrounds: 27604"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 154704.53040248112,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014533716474290509",
            "extra": "mean: 6.463934814309499 usec\nrounds: 36818"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11876306.574231064,
            "unit": "iter/sec",
            "range": "stddev: 3.694876203004706e-8",
            "extra": "mean: 84.20126187801365 nsec\nrounds: 120701"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3646.7635255348973,
            "unit": "iter/sec",
            "range": "stddev: 0.00005177277365096767",
            "extra": "mean: 274.215751308778 usec\nrounds: 1146"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 134.68843127157663,
            "unit": "iter/sec",
            "range": "stddev: 0.0023219873564306994",
            "extra": "mean: 7.4245426319033125 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156303.0944369259,
            "unit": "iter/sec",
            "range": "stddev: 0.0000025799516576305353",
            "extra": "mean: 6.397825990601467 usec\nrounds: 10896"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 15087.389162153335,
            "unit": "iter/sec",
            "range": "stddev: 0.000018246964650919163",
            "extra": "mean: 66.28052005899714 usec\nrounds: 7453"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.43848762457527,
            "unit": "iter/sec",
            "range": "stddev: 0.026153324145069844",
            "extra": "mean: 57.344422379309165 msec\nrounds: 29"
          }
        ]
      }
    ]
  }
}