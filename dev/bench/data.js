window.BENCHMARK_DATA = {
  "lastUpdate": 1768498617526,
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
          "id": "3af8ef05848ed39e622b6490876fcdd6bfea4fa2",
          "message": "Update download-artifact version in quality check workflow",
          "timestamp": "2025-04-02T21:57:27-07:00",
          "tree_id": "7def0265785a7b2208ac6f10045cddcff77c1799",
          "url": "https://github.com/iausathub/satchecker/commit/3af8ef05848ed39e622b6490876fcdd6bfea4fa2"
        },
        "date": 1743656342251,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139916.5708479455,
            "unit": "iter/sec",
            "range": "stddev: 9.608837415468114e-7",
            "extra": "mean: 7.147116270357649 usec\nrounds: 10897"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 190527.30629031127,
            "unit": "iter/sec",
            "range": "stddev: 7.478676404593848e-7",
            "extra": "mean: 5.248591498356014 usec\nrounds: 30394"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 778935.6486058345,
            "unit": "iter/sec",
            "range": "stddev: 4.010477789620387e-7",
            "extra": "mean: 1.2838030995112806 usec\nrounds: 45104"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 700983.1930517537,
            "unit": "iter/sec",
            "range": "stddev: 4.997356186428642e-7",
            "extra": "mean: 1.4265677264621235 usec\nrounds: 32491"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 325.31339825483406,
            "unit": "iter/sec",
            "range": "stddev: 0.004901606388138584",
            "extra": "mean: 3.0739588512633302 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 232.46708812306733,
            "unit": "iter/sec",
            "range": "stddev: 0.00013237693570966467",
            "extra": "mean: 4.301684200004274 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104105.99212880633,
            "unit": "iter/sec",
            "range": "stddev: 0.000014679986630330872",
            "extra": "mean: 9.605595024374182 usec\nrounds: 25283"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153933.03776987977,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010672746820142697",
            "extra": "mean: 6.49633122614612 usec\nrounds: 32428"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11543270.27950728,
            "unit": "iter/sec",
            "range": "stddev: 1.2600361145281532e-8",
            "extra": "mean: 86.63056272493832 nsec\nrounds: 116469"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3666.581014643281,
            "unit": "iter/sec",
            "range": "stddev: 0.000050043422675780344",
            "extra": "mean: 272.7336436877529 usec\nrounds: 1204"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 143.63593730132047,
            "unit": "iter/sec",
            "range": "stddev: 0.0009803601949939264",
            "extra": "mean: 6.962045980889818 msec\nrounds: 157"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156436.70723957973,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037858818746157753",
            "extra": "mean: 6.39236159879356 usec\nrounds: 10484"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16449.492090332064,
            "unit": "iter/sec",
            "range": "stddev: 0.000007541575570402093",
            "extra": "mean: 60.7921505727058 usec\nrounds: 6721"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 19.421257964022388,
            "unit": "iter/sec",
            "range": "stddev: 0.024490680063467933",
            "extra": "mean: 51.48997051851564 msec\nrounds: 27"
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
          "id": "3af8ef05848ed39e622b6490876fcdd6bfea4fa2",
          "message": "Update download-artifact version in quality check workflow",
          "timestamp": "2025-04-03T04:57:27Z",
          "url": "https://github.com/iausathub/satchecker/commit/3af8ef05848ed39e622b6490876fcdd6bfea4fa2"
        },
        "date": 1743656567559,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 137339.52515009823,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012705504099789723",
            "extra": "mean: 7.281225116419334 usec\nrounds: 11825"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 190798.62526777288,
            "unit": "iter/sec",
            "range": "stddev: 8.104818903336369e-7",
            "extra": "mean: 5.241127909577798 usec\nrounds: 41975"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 769816.4089167148,
            "unit": "iter/sec",
            "range": "stddev: 3.925581532666891e-7",
            "extra": "mean: 1.2990110218710451 usec\nrounds: 50899"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 709340.8299898778,
            "unit": "iter/sec",
            "range": "stddev: 4.243868837027087e-7",
            "extra": "mean: 1.4097595369129816 usec\nrounds: 44223"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 330.2313710647725,
            "unit": "iter/sec",
            "range": "stddev: 0.004400078912999339",
            "extra": "mean: 3.0281798993707882 msec\nrounds: 318"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 232.5981247755094,
            "unit": "iter/sec",
            "range": "stddev: 0.00014734932296374032",
            "extra": "mean: 4.299260799996318 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104387.07669052853,
            "unit": "iter/sec",
            "range": "stddev: 0.000005668424807131919",
            "extra": "mean: 9.579729902434696 usec\nrounds: 26309"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 155542.72125045664,
            "unit": "iter/sec",
            "range": "stddev: 9.993283268369543e-7",
            "extra": "mean: 6.4291018696386875 usec\nrounds: 40542"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11985863.59598428,
            "unit": "iter/sec",
            "range": "stddev: 7.978148620472546e-9",
            "extra": "mean: 83.43161858903186 nsec\nrounds: 120846"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3674.221990911547,
            "unit": "iter/sec",
            "range": "stddev: 0.00005012915069680585",
            "extra": "mean: 272.166462035656 usec\nrounds: 1238"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 145.84463743213124,
            "unit": "iter/sec",
            "range": "stddev: 0.0011452126495506846",
            "extra": "mean: 6.856611375000672 msec\nrounds: 144"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157725.77581501374,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016068136632983476",
            "extra": "mean: 6.34011780783906 usec\nrounds: 10568"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16748.132047722804,
            "unit": "iter/sec",
            "range": "stddev: 0.0000056951905180060095",
            "extra": "mean: 59.70815116280189 usec\nrounds: 7138"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.06576200225788,
            "unit": "iter/sec",
            "range": "stddev: 0.029719024635915883",
            "extra": "mean: 55.35332524999603 msec\nrounds: 12"
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
          "id": "cd97d87878b41e9a9361793fcc4cfd719040ea8c",
          "message": "Add missing section to create a folder in the quality check workflow",
          "timestamp": "2025-04-02T22:12:50-07:00",
          "tree_id": "e1270b360c7e7eae7ad886ab4fc04d9c6f86c857",
          "url": "https://github.com/iausathub/satchecker/commit/cd97d87878b41e9a9361793fcc4cfd719040ea8c"
        },
        "date": 1743657260495,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138147.600500886,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010074945099355601",
            "extra": "mean: 7.238634593538138 usec\nrounds: 10684"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187655.89276465363,
            "unit": "iter/sec",
            "range": "stddev: 8.648401294949071e-7",
            "extra": "mean: 5.328902733974561 usec\nrounds: 65583"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 754153.5419119613,
            "unit": "iter/sec",
            "range": "stddev: 4.3798045719230986e-7",
            "extra": "mean: 1.3259899270177244 usec\nrounds: 64231"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 680094.119006272,
            "unit": "iter/sec",
            "range": "stddev: 6.612306092502155e-7",
            "extra": "mean: 1.4703847188991466 usec\nrounds: 75047"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 316.28057418415943,
            "unit": "iter/sec",
            "range": "stddev: 0.0040755959333364025",
            "extra": "mean: 3.1617496666669576 msec\nrounds: 321"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.38546942141676,
            "unit": "iter/sec",
            "range": "stddev: 0.000709556239611403",
            "extra": "mean: 4.621382400000584 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 105172.85528430893,
            "unit": "iter/sec",
            "range": "stddev: 0.00001314614325673072",
            "extra": "mean: 9.50815680811124 usec\nrounds: 27658"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152127.15710879635,
            "unit": "iter/sec",
            "range": "stddev: 9.771906150778513e-7",
            "extra": "mean: 6.573448285008263 usec\nrounds: 26240"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11800692.403375747,
            "unit": "iter/sec",
            "range": "stddev: 1.5913643080002912e-8",
            "extra": "mean: 84.740790270424 nsec\nrounds: 118681"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3287.214629918237,
            "unit": "iter/sec",
            "range": "stddev: 0.00007276256299789939",
            "extra": "mean: 304.2089162352241 usec\nrounds: 1158"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 141.21780175757002,
            "unit": "iter/sec",
            "range": "stddev: 0.0016014979371638692",
            "extra": "mean: 7.081260206250128 msec\nrounds: 160"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 154883.59571911942,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017680900749901246",
            "extra": "mean: 6.456461675989849 usec\nrounds: 10620"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16620.90988017432,
            "unit": "iter/sec",
            "range": "stddev: 0.000005738410921730217",
            "extra": "mean: 60.165177911999606 usec\nrounds: 8937"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.820050349604838,
            "unit": "iter/sec",
            "range": "stddev: 0.025119680352311356",
            "extra": "mean: 56.116564228572734 msec\nrounds: 35"
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
          "id": "cd97d87878b41e9a9361793fcc4cfd719040ea8c",
          "message": "Add missing section to create a folder in the quality check workflow",
          "timestamp": "2025-04-03T05:12:50Z",
          "url": "https://github.com/iausathub/satchecker/commit/cd97d87878b41e9a9361793fcc4cfd719040ea8c"
        },
        "date": 1743657393924,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138525.20065548248,
            "unit": "iter/sec",
            "range": "stddev: 9.62047823794622e-7",
            "extra": "mean: 7.218903096823794 usec\nrounds: 11754"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 190080.53852587502,
            "unit": "iter/sec",
            "range": "stddev: 8.14342436477733e-7",
            "extra": "mean: 5.260927855924995 usec\nrounds: 45021"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 738343.5820274313,
            "unit": "iter/sec",
            "range": "stddev: 4.383649349615679e-7",
            "extra": "mean: 1.354383005882006 usec\nrounds: 56396"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 673942.0320286652,
            "unit": "iter/sec",
            "range": "stddev: 5.524542512252186e-7",
            "extra": "mean: 1.4838071413795813 usec\nrounds: 33859"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 325.72260009384223,
            "unit": "iter/sec",
            "range": "stddev: 0.004738930020983943",
            "extra": "mean: 3.07009706944466 msec\nrounds: 288"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 196.1601416874493,
            "unit": "iter/sec",
            "range": "stddev: 0.0009540058215161259",
            "extra": "mean: 5.09787559999495 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104206.32720608474,
            "unit": "iter/sec",
            "range": "stddev: 0.000004241940891252107",
            "extra": "mean: 9.596346275810484 usec\nrounds: 24905"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 133210.59540858577,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028104476370121703",
            "extra": "mean: 7.5069103695001385 usec\nrounds: 37398"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 10941326.579866843,
            "unit": "iter/sec",
            "range": "stddev: 1.8683220556377446e-8",
            "extra": "mean: 91.39659553169885 nsec\nrounds: 115648"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3667.8028055909767,
            "unit": "iter/sec",
            "range": "stddev: 0.00005048335386299388",
            "extra": "mean: 272.64279270293935 usec\nrounds: 1206"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 149.76625764250866,
            "unit": "iter/sec",
            "range": "stddev: 0.00026030026389286637",
            "extra": "mean: 6.677071429447047 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156159.37735194233,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017553014187264333",
            "extra": "mean: 6.403714057762039 usec\nrounds: 10656"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16771.45644990826,
            "unit": "iter/sec",
            "range": "stddev: 0.000005960446759609332",
            "extra": "mean: 59.62511383473019 usec\nrounds: 8934"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.54617551178917,
            "unit": "iter/sec",
            "range": "stddev: 0.024607346392397884",
            "extra": "mean: 53.91947247368247 msec\nrounds: 19"
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
          "id": "df6e32fb46bb000366c8cdc99ae4a53c1d9148be",
          "message": "Fix link to radon report and benchmark results, fix to try to get the code coverage percentage",
          "timestamp": "2025-04-02T22:34:38-07:00",
          "tree_id": "12a3668e31526984d326de542b28db1004d6ad19",
          "url": "https://github.com/iausathub/satchecker/commit/df6e32fb46bb000366c8cdc99ae4a53c1d9148be"
        },
        "date": 1743658565500,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139576.9781717304,
            "unit": "iter/sec",
            "range": "stddev: 0.000001103919936053278",
            "extra": "mean: 7.164505300936065 usec\nrounds: 11696"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 190271.3110885464,
            "unit": "iter/sec",
            "range": "stddev: 7.4756018595954e-7",
            "extra": "mean: 5.255653068657475 usec\nrounds: 61234"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 760237.7487553012,
            "unit": "iter/sec",
            "range": "stddev: 4.3377747266817966e-7",
            "extra": "mean: 1.3153779875272562 usec\nrounds: 58576"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 704035.2094395687,
            "unit": "iter/sec",
            "range": "stddev: 4.307512576974906e-7",
            "extra": "mean: 1.4203835072340023 usec\nrounds: 57965"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 329.0358797605157,
            "unit": "iter/sec",
            "range": "stddev: 0.004475133610106245",
            "extra": "mean: 3.0391822336452687 msec\nrounds: 321"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 218.31531919015254,
            "unit": "iter/sec",
            "range": "stddev: 0.0007102890768674832",
            "extra": "mean: 4.580530600003385 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 106184.91306107263,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037888817298780546",
            "extra": "mean: 9.41753372651769 usec\nrounds: 27130"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152418.79324346466,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010205685952470119",
            "extra": "mean: 6.56087073463874 usec\nrounds: 30449"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12156472.454304928,
            "unit": "iter/sec",
            "range": "stddev: 8.263616202725092e-9",
            "extra": "mean: 82.2607054603079 nsec\nrounds: 121566"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3624.761465706514,
            "unit": "iter/sec",
            "range": "stddev: 0.00004916541708520636",
            "extra": "mean: 275.8802225914435 usec\nrounds: 1204"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.61811041630173,
            "unit": "iter/sec",
            "range": "stddev: 0.0002939539819912208",
            "extra": "mean: 6.728655055557153 msec\nrounds: 162"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156555.94517906365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016121224423446658",
            "extra": "mean: 6.387492974835495 usec\nrounds: 10818"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 14927.50567487762,
            "unit": "iter/sec",
            "range": "stddev: 0.000018426798306400015",
            "extra": "mean: 66.99042839306763 usec\nrounds: 8805"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 20.634185341457407,
            "unit": "iter/sec",
            "range": "stddev: 0.023511617152351755",
            "extra": "mean: 48.46326537500071 msec\nrounds: 24"
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
          "id": "df6e32fb46bb000366c8cdc99ae4a53c1d9148be",
          "message": "Fix link to radon report and benchmark results, fix to try to get the code coverage percentage",
          "timestamp": "2025-04-03T05:34:38Z",
          "url": "https://github.com/iausathub/satchecker/commit/df6e32fb46bb000366c8cdc99ae4a53c1d9148be"
        },
        "date": 1743658585231,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 141514.64741848645,
            "unit": "iter/sec",
            "range": "stddev: 9.050563775789552e-7",
            "extra": "mean: 7.066406327839722 usec\nrounds: 12042"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186904.7164320136,
            "unit": "iter/sec",
            "range": "stddev: 7.841595581609306e-7",
            "extra": "mean: 5.350319773036594 usec\nrounds: 60274"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 748879.7604576577,
            "unit": "iter/sec",
            "range": "stddev: 4.2941362401478564e-7",
            "extra": "mean: 1.3353278494118694 usec\nrounds: 64856"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 708275.0309687478,
            "unit": "iter/sec",
            "range": "stddev: 4.791884464067501e-7",
            "extra": "mean: 1.4118809167001745 usec\nrounds: 66147"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 334.8067180057817,
            "unit": "iter/sec",
            "range": "stddev: 0.003933295286273373",
            "extra": "mean: 2.986797893292963 msec\nrounds: 328"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.26383634386946,
            "unit": "iter/sec",
            "range": "stddev: 0.00039865560471010457",
            "extra": "mean: 4.62398160000248 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 95756.91860124945,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034304590742552665",
            "extra": "mean: 10.443109642700554 usec\nrounds: 15587"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 154064.3147150323,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010152362110159683",
            "extra": "mean: 6.490795755328981 usec\nrounds: 24549"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12220062.211240217,
            "unit": "iter/sec",
            "range": "stddev: 9.940036001336871e-9",
            "extra": "mean: 81.83264395177326 nsec\nrounds: 120978"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3595.841855357641,
            "unit": "iter/sec",
            "range": "stddev: 0.000049810575408455935",
            "extra": "mean: 278.0989932886079 usec\nrounds: 1192"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.46441619347928,
            "unit": "iter/sec",
            "range": "stddev: 0.0003765433790107747",
            "extra": "mean: 6.735620734175096 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156713.22055976518,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018320233255747443",
            "extra": "mean: 6.381082568707938 usec\nrounds: 10682"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16547.77511506657,
            "unit": "iter/sec",
            "range": "stddev: 0.00001178196633475252",
            "extra": "mean: 60.43108472567474 usec\nrounds: 8439"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.309666227844396,
            "unit": "iter/sec",
            "range": "stddev: 0.023528881421649214",
            "extra": "mean: 57.77118904761989 msec\nrounds: 42"
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
          "id": "3862cbec5ebd691bb95dc9b187dc70bd30dbce12",
          "message": "change complexity report format",
          "timestamp": "2025-04-02T23:08:40-07:00",
          "tree_id": "b148b4b7d9beb317342225f6b84595e2d50e12fe",
          "url": "https://github.com/iausathub/satchecker/commit/3862cbec5ebd691bb95dc9b187dc70bd30dbce12"
        },
        "date": 1743660618966,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 141683.60733862914,
            "unit": "iter/sec",
            "range": "stddev: 9.891207179181425e-7",
            "extra": "mean: 7.0579795276525 usec\nrounds: 11088"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 190669.00443889154,
            "unit": "iter/sec",
            "range": "stddev: 8.982972480869731e-7",
            "extra": "mean: 5.2446909393733945 usec\nrounds: 39688"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 773274.7253787195,
            "unit": "iter/sec",
            "range": "stddev: 4.1639946536221084e-7",
            "extra": "mean: 1.2932014550329953 usec\nrounds: 28453"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 704259.9169534573,
            "unit": "iter/sec",
            "range": "stddev: 5.330086278620286e-7",
            "extra": "mean: 1.4199303068757316 usec\nrounds: 20375"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 320.72232956081814,
            "unit": "iter/sec",
            "range": "stddev: 0.005612828601902954",
            "extra": "mean: 3.1179618873726453 msec\nrounds: 293"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 228.651579442803,
            "unit": "iter/sec",
            "range": "stddev: 0.00009680292833854594",
            "extra": "mean: 4.37346639999987 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 97694.2112112025,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032494988449601504",
            "extra": "mean: 10.236021025218442 usec\nrounds: 17598"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153493.94503539652,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010194159772126552",
            "extra": "mean: 6.514914967944792 usec\nrounds: 29777"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12183881.779772356,
            "unit": "iter/sec",
            "range": "stddev: 8.83335748147558e-9",
            "extra": "mean: 82.07564863774209 nsec\nrounds: 120121"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3636.751810583668,
            "unit": "iter/sec",
            "range": "stddev: 0.00005044843868017905",
            "extra": "mean: 274.9706474579326 usec\nrounds: 1180"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 135.9223064104809,
            "unit": "iter/sec",
            "range": "stddev: 0.002514322890727723",
            "extra": "mean: 7.357144139241082 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 144340.22561374874,
            "unit": "iter/sec",
            "range": "stddev: 0.00008286757244238426",
            "extra": "mean: 6.928075633441075 usec\nrounds: 10498"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16870.736483526078,
            "unit": "iter/sec",
            "range": "stddev: 0.000005436834259970996",
            "extra": "mean: 59.2742350623803 usec\nrounds: 6862"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 16.548949849151256,
            "unit": "iter/sec",
            "range": "stddev: 0.02808865427144941",
            "extra": "mean: 60.426795000003395 msec\nrounds: 13"
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
          "id": "3862cbec5ebd691bb95dc9b187dc70bd30dbce12",
          "message": "change complexity report format",
          "timestamp": "2025-04-03T06:08:40Z",
          "url": "https://github.com/iausathub/satchecker/commit/3862cbec5ebd691bb95dc9b187dc70bd30dbce12"
        },
        "date": 1743660806860,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139300.1277586131,
            "unit": "iter/sec",
            "range": "stddev: 9.206336714799311e-7",
            "extra": "mean: 7.178744313378196 usec\nrounds: 11870"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 188317.73391485447,
            "unit": "iter/sec",
            "range": "stddev: 8.2307117125916e-7",
            "extra": "mean: 5.31017434848774 usec\nrounds: 42134"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 758318.6841125735,
            "unit": "iter/sec",
            "range": "stddev: 4.3110393329794624e-7",
            "extra": "mean: 1.3187067930025427 usec\nrounds: 47284"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 690094.9200869885,
            "unit": "iter/sec",
            "range": "stddev: 4.3274271796281886e-7",
            "extra": "mean: 1.4490760196784915 usec\nrounds: 43173"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 322.63444530008155,
            "unit": "iter/sec",
            "range": "stddev: 0.004905174292226359",
            "extra": "mean: 3.0994830668805444 msec\nrounds: 314"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 221.29679835314295,
            "unit": "iter/sec",
            "range": "stddev: 0.0003903703802789581",
            "extra": "mean: 4.518818200000396 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 99242.75463871981,
            "unit": "iter/sec",
            "range": "stddev: 0.000003286778713284349",
            "extra": "mean: 10.07630233199762 usec\nrounds: 18096"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153425.69525082174,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011162879984553002",
            "extra": "mean: 6.5178130584006215 usec\nrounds: 32791"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11954645.734730173,
            "unit": "iter/sec",
            "range": "stddev: 8.863103902900957e-9",
            "extra": "mean: 83.64948842395522 nsec\nrounds: 120686"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3639.740630204569,
            "unit": "iter/sec",
            "range": "stddev: 0.0000494934722949669",
            "extra": "mean: 274.74485179011117 usec\nrounds: 1201"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.43985774452827,
            "unit": "iter/sec",
            "range": "stddev: 0.0002453446190199792",
            "extra": "mean: 6.73673510062941 msec\nrounds: 159"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 148267.82554636017,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018587162544540452",
            "extra": "mean: 6.74455159988383 usec\nrounds: 10281"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16594.1666146094,
            "unit": "iter/sec",
            "range": "stddev: 0.000009261156394952646",
            "extra": "mean: 60.26214049939732 usec\nrounds: 8968"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 14.985138686239223,
            "unit": "iter/sec",
            "range": "stddev: 0.026956998842171707",
            "extra": "mean: 66.73278245454578 msec\nrounds: 11"
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
          "id": "69f5334553244941f97213ff0316ac5c4e59ea94",
          "message": "Fix links to coverage and benchmark reports",
          "timestamp": "2025-04-03T09:27:25-07:00",
          "tree_id": "0f57a102ffd4edf58d05a48b9051fec5cf64ed77",
          "url": "https://github.com/iausathub/satchecker/commit/69f5334553244941f97213ff0316ac5c4e59ea94"
        },
        "date": 1743697740440,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 113974.4589696917,
            "unit": "iter/sec",
            "range": "stddev: 0.000003963156811864519",
            "extra": "mean: 8.77389556432044 usec\nrounds: 11768"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 162400.8610941058,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019603221680256647",
            "extra": "mean: 6.157602818500659 usec\nrounds: 39098"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 661055.6796157717,
            "unit": "iter/sec",
            "range": "stddev: 8.917647414864433e-7",
            "extra": "mean: 1.5127318784723767 usec\nrounds: 33496"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 609875.7350256433,
            "unit": "iter/sec",
            "range": "stddev: 7.536094430578613e-7",
            "extra": "mean: 1.6396782861970287 usec\nrounds: 54219"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 332.8217821067847,
            "unit": "iter/sec",
            "range": "stddev: 0.004265543420332979",
            "extra": "mean: 3.0046110373844264 msec\nrounds: 321"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 215.9813779128223,
            "unit": "iter/sec",
            "range": "stddev: 0.0006923342134897113",
            "extra": "mean: 4.630028799999764 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 99848.31442049105,
            "unit": "iter/sec",
            "range": "stddev: 0.000007900356255277891",
            "extra": "mean: 10.015191601419547 usec\nrounds: 18622"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153179.9728288781,
            "unit": "iter/sec",
            "range": "stddev: 0.00000103184457129521",
            "extra": "mean: 6.528268555819173 usec\nrounds: 24561"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12050394.272664625,
            "unit": "iter/sec",
            "range": "stddev: 8.440834539290035e-9",
            "extra": "mean: 82.98483662635216 nsec\nrounds: 119389"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3660.443854200276,
            "unit": "iter/sec",
            "range": "stddev: 0.000050520801259596674",
            "extra": "mean: 273.19091340590376 usec\nrounds: 1201"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 150.82001661904442,
            "unit": "iter/sec",
            "range": "stddev: 0.00017372532194630906",
            "extra": "mean: 6.63041963803714 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 153841.92149435455,
            "unit": "iter/sec",
            "range": "stddev: 0.000003320644736380038",
            "extra": "mean: 6.500178821782958 usec\nrounds: 9982"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16691.334382974055,
            "unit": "iter/sec",
            "range": "stddev: 0.000005446828089285773",
            "extra": "mean: 59.91132746223376 usec\nrounds: 8630"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.952409727198525,
            "unit": "iter/sec",
            "range": "stddev: 0.027295413884886436",
            "extra": "mean: 52.763738985913974 msec\nrounds: 71"
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
          "id": "69f5334553244941f97213ff0316ac5c4e59ea94",
          "message": "Fix links to coverage and benchmark reports",
          "timestamp": "2025-04-03T16:27:25Z",
          "url": "https://github.com/iausathub/satchecker/commit/69f5334553244941f97213ff0316ac5c4e59ea94"
        },
        "date": 1743697771016,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 140839.31509648697,
            "unit": "iter/sec",
            "range": "stddev: 8.57885936244726e-7",
            "extra": "mean: 7.100290137841941 usec\nrounds: 11529"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187833.61472248254,
            "unit": "iter/sec",
            "range": "stddev: 8.824895752953631e-7",
            "extra": "mean: 5.323860702342678 usec\nrounds: 63533"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 748938.0182185445,
            "unit": "iter/sec",
            "range": "stddev: 4.6491277516432975e-7",
            "extra": "mean: 1.335223978051805 usec\nrounds: 43473"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 684543.7545056088,
            "unit": "iter/sec",
            "range": "stddev: 4.4558493371612046e-7",
            "extra": "mean: 1.4608270010763884 usec\nrounds: 67486"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 333.4601874028072,
            "unit": "iter/sec",
            "range": "stddev: 0.004237086537332181",
            "extra": "mean: 2.9988587476922337 msec\nrounds: 325"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 218.13386997730302,
            "unit": "iter/sec",
            "range": "stddev: 0.0007295448056332577",
            "extra": "mean: 4.584340800005293 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 106175.1871353361,
            "unit": "iter/sec",
            "range": "stddev: 0.000014661151120897184",
            "extra": "mean: 9.418396397317869 usec\nrounds: 27036"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152078.50682272157,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012733034749545547",
            "extra": "mean: 6.575551147182839 usec\nrounds: 30422"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12204181.443148453,
            "unit": "iter/sec",
            "range": "stddev: 8.753496204882728e-9",
            "extra": "mean: 81.9391291958535 nsec\nrounds: 67765"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3716.5289917718505,
            "unit": "iter/sec",
            "range": "stddev: 0.000050254708621906695",
            "extra": "mean: 269.06826294478907 usec\nrounds: 1236"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 150.40490634015177,
            "unit": "iter/sec",
            "range": "stddev: 0.00043409150585210337",
            "extra": "mean: 6.6487192760748535 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 152338.2404405844,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018338095554059735",
            "extra": "mean: 6.564339965512626 usec\nrounds: 10404"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16866.841706065286,
            "unit": "iter/sec",
            "range": "stddev: 0.000004941305225088728",
            "extra": "mean: 59.287922269431256 usec\nrounds: 7050"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.62325637956106,
            "unit": "iter/sec",
            "range": "stddev: 0.03085182917941692",
            "extra": "mean: 56.743202190474335 msec\nrounds: 21"
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
          "id": "939f4df7c562844e46befcc28a809eab9b9911c1",
          "message": "Fix directory name for coverage report",
          "timestamp": "2025-04-03T09:34:12-07:00",
          "tree_id": "99e6b9f4d57d11b901a4efc4878756e20f21ff97",
          "url": "https://github.com/iausathub/satchecker/commit/939f4df7c562844e46befcc28a809eab9b9911c1"
        },
        "date": 1743698138327,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 120460.66029268221,
            "unit": "iter/sec",
            "range": "stddev: 0.000003583394790536593",
            "extra": "mean: 8.3014653711038 usec\nrounds: 11320"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 160957.82707665116,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027823453480462393",
            "extra": "mean: 6.212807529538661 usec\nrounds: 9695"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 664087.5393768754,
            "unit": "iter/sec",
            "range": "stddev: 6.926749896074175e-7",
            "extra": "mean: 1.5058255737463724 usec\nrounds: 37695"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 616311.8303251171,
            "unit": "iter/sec",
            "range": "stddev: 8.051510677747428e-7",
            "extra": "mean: 1.6225552566019696 usec\nrounds: 53894"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 321.0865050023142,
            "unit": "iter/sec",
            "range": "stddev: 0.0046053300448005135",
            "extra": "mean: 3.1144255034723205 msec\nrounds: 288"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.10244120080802,
            "unit": "iter/sec",
            "range": "stddev: 0.0007481873276250324",
            "extra": "mean: 4.627435000008973 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 103077.67192182915,
            "unit": "iter/sec",
            "range": "stddev: 0.000002778285271359586",
            "extra": "mean: 9.70142205732361 usec\nrounds: 26295"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 149718.51680366433,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010061470092463351",
            "extra": "mean: 6.679200551467961 usec\nrounds: 33722"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11957589.036115037,
            "unit": "iter/sec",
            "range": "stddev: 9.506329918486656e-9",
            "extra": "mean: 83.62889851622644 nsec\nrounds: 116334"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3595.7657910943017,
            "unit": "iter/sec",
            "range": "stddev: 0.00005023879140551201",
            "extra": "mean: 278.10487615092126 usec\nrounds: 1195"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 146.53758725839015,
            "unit": "iter/sec",
            "range": "stddev: 0.0002847644411815289",
            "extra": "mean: 6.82418769620314 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157577.67543946012,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017756669654487798",
            "extra": "mean: 6.34607660768667 usec\nrounds: 10495"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16687.227264511683,
            "unit": "iter/sec",
            "range": "stddev: 0.00000702308434678764",
            "extra": "mean: 59.926073046699344 usec\nrounds: 8652"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.52135671855713,
            "unit": "iter/sec",
            "range": "stddev: 0.025454610580962305",
            "extra": "mean: 53.991725076925306 msec\nrounds: 13"
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
          "id": "939f4df7c562844e46befcc28a809eab9b9911c1",
          "message": "Fix directory name for coverage report",
          "timestamp": "2025-04-03T16:34:12Z",
          "url": "https://github.com/iausathub/satchecker/commit/939f4df7c562844e46befcc28a809eab9b9911c1"
        },
        "date": 1743698213309,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138740.1392538461,
            "unit": "iter/sec",
            "range": "stddev: 8.912603145566497e-7",
            "extra": "mean: 7.207719448589773 usec\nrounds: 11677"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 188277.84546466728,
            "unit": "iter/sec",
            "range": "stddev: 7.569394220035255e-7",
            "extra": "mean: 5.311299359369729 usec\nrounds: 52285"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 760822.4886536527,
            "unit": "iter/sec",
            "range": "stddev: 3.739535036267532e-7",
            "extra": "mean: 1.314367036875572 usec\nrounds: 56809"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 696695.7156625881,
            "unit": "iter/sec",
            "range": "stddev: 4.5307611112034655e-7",
            "extra": "mean: 1.4353468487300172 usec\nrounds: 80822"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 334.7303293167999,
            "unit": "iter/sec",
            "range": "stddev: 0.0041178272169686446",
            "extra": "mean: 2.987479509374147 msec\nrounds: 320"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 157.03547180080454,
            "unit": "iter/sec",
            "range": "stddev: 0.0027025916775499175",
            "extra": "mean: 6.367987999988145 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 102990.2855807152,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030583300121757496",
            "extra": "mean: 9.709653627635427 usec\nrounds: 21832"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 151659.62359785545,
            "unit": "iter/sec",
            "range": "stddev: 9.97547614782681e-7",
            "extra": "mean: 6.593712791030167 usec\nrounds: 35072"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11790958.368821846,
            "unit": "iter/sec",
            "range": "stddev: 8.386314856848809e-9",
            "extra": "mean: 84.81074809353188 nsec\nrounds: 118274"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3647.5584159740106,
            "unit": "iter/sec",
            "range": "stddev: 0.00004904785174179491",
            "extra": "mean: 274.15599312148896 usec\nrounds: 1163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.74134959795538,
            "unit": "iter/sec",
            "range": "stddev: 0.00023344421246508418",
            "extra": "mean: 6.723080049380876 msec\nrounds: 162"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157236.03425451272,
            "unit": "iter/sec",
            "range": "stddev: 0.000002828605637931749",
            "extra": "mean: 6.359865311671073 usec\nrounds: 11122"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16901.751172057437,
            "unit": "iter/sec",
            "range": "stddev: 0.0000061168007786437074",
            "extra": "mean: 59.165466928257395 usec\nrounds: 9419"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.31437644155615,
            "unit": "iter/sec",
            "range": "stddev: 0.023081598100234635",
            "extra": "mean: 57.75547293750094 msec\nrounds: 16"
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
          "id": "13521f0351aa20d404291ed15eac4216875eefef",
          "message": "Debugging to see why coverage% isn't working",
          "timestamp": "2025-04-03T09:53:13-07:00",
          "tree_id": "dce7c9858eaf64eef09c41a9d8618361a9db6ac2",
          "url": "https://github.com/iausathub/satchecker/commit/13521f0351aa20d404291ed15eac4216875eefef"
        },
        "date": 1743699285463,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138144.94947983057,
            "unit": "iter/sec",
            "range": "stddev: 9.283740028298985e-7",
            "extra": "mean: 7.238773503956451 usec\nrounds: 11647"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186604.5307523144,
            "unit": "iter/sec",
            "range": "stddev: 8.000200657516691e-7",
            "extra": "mean: 5.358926688266369 usec\nrounds: 39830"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 769183.9017164945,
            "unit": "iter/sec",
            "range": "stddev: 3.749945539180366e-7",
            "extra": "mean: 1.3000792109252695 usec\nrounds: 42330"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 675571.9162907212,
            "unit": "iter/sec",
            "range": "stddev: 4.757266228020766e-7",
            "extra": "mean: 1.4802273094633298 usec\nrounds: 38375"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 314.7478916905716,
            "unit": "iter/sec",
            "range": "stddev: 0.004783652011231585",
            "extra": "mean: 3.177145983818374 msec\nrounds: 309"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 214.6232430621543,
            "unit": "iter/sec",
            "range": "stddev: 0.0007475331479245549",
            "extra": "mean: 4.659327599995322 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 96350.07576256408,
            "unit": "iter/sec",
            "range": "stddev: 0.000019969438577241474",
            "extra": "mean: 10.378819031386175 usec\nrounds: 16804"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 148334.2233619857,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011606280284135126",
            "extra": "mean: 6.741532583210158 usec\nrounds: 23816"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 10804259.808461921,
            "unit": "iter/sec",
            "range": "stddev: 1.9585625139955215e-8",
            "extra": "mean: 92.55608600016832 nsec\nrounds: 64604"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3147.978973132027,
            "unit": "iter/sec",
            "range": "stddev: 0.00012205110773319764",
            "extra": "mean: 317.66412944145793 usec\nrounds: 1182"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 138.06866602065764,
            "unit": "iter/sec",
            "range": "stddev: 0.0014142065869682066",
            "extra": "mean: 7.242772953643091 msec\nrounds: 151"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157944.1535117869,
            "unit": "iter/sec",
            "range": "stddev: 0.000001648208182647318",
            "extra": "mean: 6.331351795971181 usec\nrounds: 10580"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16683.06917482881,
            "unit": "iter/sec",
            "range": "stddev: 0.00000646326210784982",
            "extra": "mean: 59.941009026611624 usec\nrounds: 8641"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.20561483626319,
            "unit": "iter/sec",
            "range": "stddev: 0.025998783120170985",
            "extra": "mean: 54.92810921211688 msec\nrounds: 66"
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
          "id": "13521f0351aa20d404291ed15eac4216875eefef",
          "message": "Debugging to see why coverage% isn't working",
          "timestamp": "2025-04-03T16:53:13Z",
          "url": "https://github.com/iausathub/satchecker/commit/13521f0351aa20d404291ed15eac4216875eefef"
        },
        "date": 1743699295965,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138639.73280471595,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010394424634828373",
            "extra": "mean: 7.212939463815702 usec\nrounds: 11712"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187369.8923444464,
            "unit": "iter/sec",
            "range": "stddev: 8.094603480635731e-7",
            "extra": "mean: 5.33703674313735 usec\nrounds: 45723"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 752889.5943475494,
            "unit": "iter/sec",
            "range": "stddev: 4.7095858360721793e-7",
            "extra": "mean: 1.3282159927666357 usec\nrounds: 43895"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 698257.4444818685,
            "unit": "iter/sec",
            "range": "stddev: 5.227419195938141e-7",
            "extra": "mean: 1.4321365391843908 usec\nrounds: 20961"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 323.2850137497049,
            "unit": "iter/sec",
            "range": "stddev: 0.004681058016161764",
            "extra": "mean: 3.0932457660231174 msec\nrounds: 312"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.55325267543554,
            "unit": "iter/sec",
            "range": "stddev: 0.0007340447047228816",
            "extra": "mean: 4.617801799997778 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 101191.80444615656,
            "unit": "iter/sec",
            "range": "stddev: 0.000016210280626424326",
            "extra": "mean: 9.882223224234458 usec\nrounds: 22511"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 151724.76674999876,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012499385109369845",
            "extra": "mean: 6.590881775074525 usec\nrounds: 34502"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11947350.850865835,
            "unit": "iter/sec",
            "range": "stddev: 1.0005684114806201e-8",
            "extra": "mean: 83.70056362135671 nsec\nrounds: 66676"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3619.51453568522,
            "unit": "iter/sec",
            "range": "stddev: 0.00004993889941217255",
            "extra": "mean: 276.28014479314345 usec\nrounds: 1181"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 146.21832080670032,
            "unit": "iter/sec",
            "range": "stddev: 0.0002958564845299319",
            "extra": "mean: 6.839088251615155 msec\nrounds: 155"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 129358.08486329675,
            "unit": "iter/sec",
            "range": "stddev: 0.00005624012413325876",
            "extra": "mean: 7.730479320691719 usec\nrounds: 9720"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16758.246278051545,
            "unit": "iter/sec",
            "range": "stddev: 0.000005859401237222409",
            "extra": "mean: 59.6721150535728 usec\nrounds: 8596"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 16.776367324837278,
            "unit": "iter/sec",
            "range": "stddev: 0.02509454865507402",
            "extra": "mean: 59.607660027776575 msec\nrounds: 36"
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
          "id": "8abd72da7a00e7a1688bd948e97cab63161c9f6d",
          "message": "Remove debugging steps for coverage percentage",
          "timestamp": "2025-04-03T11:30:50-07:00",
          "tree_id": "fdfe0df64658b4ae0a549ae40ed890ac0c5888de",
          "url": "https://github.com/iausathub/satchecker/commit/8abd72da7a00e7a1688bd948e97cab63161c9f6d"
        },
        "date": 1743705140789,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 140457.04132540646,
            "unit": "iter/sec",
            "range": "stddev: 8.70518141139959e-7",
            "extra": "mean: 7.119614585097456 usec\nrounds: 11834"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186987.90908925064,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010507504091188493",
            "extra": "mean: 5.347939366083253 usec\nrounds: 52149"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 764962.5903908428,
            "unit": "iter/sec",
            "range": "stddev: 4.1127743747599803e-7",
            "extra": "mean: 1.307253469073657 usec\nrounds: 67669"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 681608.0944438506,
            "unit": "iter/sec",
            "range": "stddev: 5.666710675075684e-7",
            "extra": "mean: 1.4671187272444837 usec\nrounds: 66278"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 319.4252632504345,
            "unit": "iter/sec",
            "range": "stddev: 0.004303667279361416",
            "extra": "mean: 3.1306227623454568 msec\nrounds: 324"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 218.77303680078163,
            "unit": "iter/sec",
            "range": "stddev: 0.0007348960820620882",
            "extra": "mean: 4.570947199999864 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 106902.94633950775,
            "unit": "iter/sec",
            "range": "stddev: 0.000014000411372041527",
            "extra": "mean: 9.354279131130303 usec\nrounds: 28406"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153583.01046268325,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011930583714603604",
            "extra": "mean: 6.51113685678778 usec\nrounds: 40641"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11928938.767767645,
            "unit": "iter/sec",
            "range": "stddev: 1.0088196422141417e-8",
            "extra": "mean: 83.82975380017731 nsec\nrounds: 66450"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3318.7949058095805,
            "unit": "iter/sec",
            "range": "stddev: 0.00007123675449423995",
            "extra": "mean: 301.3141903555086 usec\nrounds: 1182"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 123.68812471025375,
            "unit": "iter/sec",
            "range": "stddev: 0.00339885788795616",
            "extra": "mean: 8.08485052500032 msec\nrounds: 160"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 153692.4498864601,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015665475013161053",
            "extra": "mean: 6.506500486775684 usec\nrounds: 10270"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16707.035464137687,
            "unit": "iter/sec",
            "range": "stddev: 0.000006434905518804419",
            "extra": "mean: 59.8550234807689 usec\nrounds: 9412"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 19.263771791855554,
            "unit": "iter/sec",
            "range": "stddev: 0.023220948192707258",
            "extra": "mean: 51.91091395833425 msec\nrounds: 24"
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
          "id": "8abd72da7a00e7a1688bd948e97cab63161c9f6d",
          "message": "Remove debugging steps for coverage percentage",
          "timestamp": "2025-04-03T18:30:50Z",
          "url": "https://github.com/iausathub/satchecker/commit/8abd72da7a00e7a1688bd948e97cab63161c9f6d"
        },
        "date": 1743705205632,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139650.0216334938,
            "unit": "iter/sec",
            "range": "stddev: 9.610380351488936e-7",
            "extra": "mean: 7.160757931169265 usec\nrounds: 11253"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187989.3793124401,
            "unit": "iter/sec",
            "range": "stddev: 7.977408729391525e-7",
            "extra": "mean: 5.319449447928601 usec\nrounds: 65665"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 760404.5793003436,
            "unit": "iter/sec",
            "range": "stddev: 4.094687707261102e-7",
            "extra": "mean: 1.315089397436442 usec\nrounds: 52261"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 678022.3906409506,
            "unit": "iter/sec",
            "range": "stddev: 5.52628006786176e-7",
            "extra": "mean: 1.4748775465286277 usec\nrounds: 50901"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 316.35387169137994,
            "unit": "iter/sec",
            "range": "stddev: 0.0051327403813473576",
            "extra": "mean: 3.1610171061081664 msec\nrounds: 311"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 217.43937735828018,
            "unit": "iter/sec",
            "range": "stddev: 0.0007587144157113477",
            "extra": "mean: 4.59898299999395 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 96597.88063122601,
            "unit": "iter/sec",
            "range": "stddev: 0.000017688548493408262",
            "extra": "mean: 10.352193997067285 usec\nrounds: 22789"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 154658.3727783348,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010495970622859365",
            "extra": "mean: 6.465863968666326 usec\nrounds: 26413"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11261722.026143774,
            "unit": "iter/sec",
            "range": "stddev: 8.370414536275701e-9",
            "extra": "mean: 88.79636681486201 nsec\nrounds: 112411"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3631.1034218908326,
            "unit": "iter/sec",
            "range": "stddev: 0.000050734750975135436",
            "extra": "mean: 275.39837999967176 usec\nrounds: 1200"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 144.59017865375088,
            "unit": "iter/sec",
            "range": "stddev: 0.0007856938051376539",
            "extra": "mean: 6.916099069181546 msec\nrounds: 159"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156475.91738969923,
            "unit": "iter/sec",
            "range": "stddev: 0.000001723626710300702",
            "extra": "mean: 6.3907597838811565 usec\nrounds: 10732"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16440.500773346077,
            "unit": "iter/sec",
            "range": "stddev: 0.000008774535474373288",
            "extra": "mean: 60.82539782615597 usec\nrounds: 8740"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 19.741118516771344,
            "unit": "iter/sec",
            "range": "stddev: 0.025417713539166328",
            "extra": "mean: 50.65569102127805 msec\nrounds: 47"
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
          "id": "8abd72da7a00e7a1688bd948e97cab63161c9f6d",
          "message": "Remove debugging steps for coverage percentage",
          "timestamp": "2025-04-03T18:30:50Z",
          "url": "https://github.com/iausathub/satchecker/commit/8abd72da7a00e7a1688bd948e97cab63161c9f6d"
        },
        "date": 1743723024792,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 125147.52537811508,
            "unit": "iter/sec",
            "range": "stddev: 0.000002723787893262275",
            "extra": "mean: 7.990569505698535 usec\nrounds: 11884"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 184343.2167855295,
            "unit": "iter/sec",
            "range": "stddev: 0.000001058841680861129",
            "extra": "mean: 5.4246639363108775 usec\nrounds: 48833"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 764472.8923970301,
            "unit": "iter/sec",
            "range": "stddev: 4.14213083218654e-7",
            "extra": "mean: 1.308090855732591 usec\nrounds: 63056"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 697509.499893961,
            "unit": "iter/sec",
            "range": "stddev: 4.526120948881935e-7",
            "extra": "mean: 1.4336722297718172 usec\nrounds: 66989"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 331.75263112643006,
            "unit": "iter/sec",
            "range": "stddev: 0.004265069290973081",
            "extra": "mean: 3.014294104027475 msec\nrounds: 298"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.59541038609927,
            "unit": "iter/sec",
            "range": "stddev: 0.0007274538747041766",
            "extra": "mean: 4.6169030000100975 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 105763.34250695644,
            "unit": "iter/sec",
            "range": "stddev: 0.000013378893474628658",
            "extra": "mean: 9.455071826367687 usec\nrounds: 26940"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152667.49457555084,
            "unit": "iter/sec",
            "range": "stddev: 9.297833830920164e-7",
            "extra": "mean: 6.550182819075007 usec\nrounds: 38054"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11612287.088855352,
            "unit": "iter/sec",
            "range": "stddev: 1.0279439483903375e-8",
            "extra": "mean: 86.11568008506931 nsec\nrounds: 65536"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3625.773861688311,
            "unit": "iter/sec",
            "range": "stddev: 0.000055597811619544124",
            "extra": "mean: 275.80319075232075 usec\nrounds: 1211"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 150.43365449589294,
            "unit": "iter/sec",
            "range": "stddev: 0.0003435287769690094",
            "extra": "mean: 6.647448693253021 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 158111.2919081531,
            "unit": "iter/sec",
            "range": "stddev: 0.0000030702885235948717",
            "extra": "mean: 6.324658966045893 usec\nrounds: 10779"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16770.418800669093,
            "unit": "iter/sec",
            "range": "stddev: 0.000005804123472811704",
            "extra": "mean: 59.62880306603331 usec\nrounds: 8871"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 16.957838692257813,
            "unit": "iter/sec",
            "range": "stddev: 0.02020465259317225",
            "extra": "mean: 58.96977899999456 msec\nrounds: 12"
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
          "id": "601726330c3e9a28ff03f762555121459d147932",
          "message": "Add initial codecov step",
          "timestamp": "2025-04-03T17:34:42-07:00",
          "tree_id": "daef6dd11c75ade1538d09d263d103b928d3f44e",
          "url": "https://github.com/iausathub/satchecker/commit/601726330c3e9a28ff03f762555121459d147932"
        },
        "date": 1743726974910,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139541.8183679779,
            "unit": "iter/sec",
            "range": "stddev: 8.533580964989991e-7",
            "extra": "mean: 7.166310513189359 usec\nrounds: 12270"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 189342.47948260856,
            "unit": "iter/sec",
            "range": "stddev: 7.662114105194931e-7",
            "extra": "mean: 5.281435009896191 usec\nrounds: 64479"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 744629.4061204297,
            "unit": "iter/sec",
            "range": "stddev: 4.829007044105149e-7",
            "extra": "mean: 1.3429499181479665 usec\nrounds: 50058"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 704868.4862624222,
            "unit": "iter/sec",
            "range": "stddev: 4.247185787665202e-7",
            "extra": "mean: 1.4187043675374367 usec\nrounds: 56073"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 317.5759217129034,
            "unit": "iter/sec",
            "range": "stddev: 0.004116421170187079",
            "extra": "mean: 3.1488533343659006 msec\nrounds: 323"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 217.10399081418325,
            "unit": "iter/sec",
            "range": "stddev: 0.0007257414172451333",
            "extra": "mean: 4.606087600001274 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 105122.31584001303,
            "unit": "iter/sec",
            "range": "stddev: 0.000002905188881806962",
            "extra": "mean: 9.512728025530874 usec\nrounds: 27168"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152606.02158348667,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010628081426408057",
            "extra": "mean: 6.5528213737812875 usec\nrounds: 33892"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11912767.854969606,
            "unit": "iter/sec",
            "range": "stddev: 3.5973183964699286e-8",
            "extra": "mean: 83.94354797939116 nsec\nrounds: 122760"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3622.0908698829194,
            "unit": "iter/sec",
            "range": "stddev: 0.000049918515874575444",
            "extra": "mean: 276.08363122936345 usec\nrounds: 1204"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 120.20322446178083,
            "unit": "iter/sec",
            "range": "stddev: 0.0037883673935626343",
            "extra": "mean: 8.319244383647582 msec\nrounds: 159"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 153079.49632993212,
            "unit": "iter/sec",
            "range": "stddev: 0.000012717821758494536",
            "extra": "mean: 6.532553503081176 usec\nrounds: 10448"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16500.833967131355,
            "unit": "iter/sec",
            "range": "stddev: 0.000008499176396507909",
            "extra": "mean: 60.60299752072764 usec\nrounds: 6453"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 20.129988740881483,
            "unit": "iter/sec",
            "range": "stddev: 0.028971925814490627",
            "extra": "mean: 49.67712664285427 msec\nrounds: 14"
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
          "id": "7768f23328bf31434be013f7878427f73e4919e7",
          "message": "Allow code coverage workflow to run on workflow dispatch",
          "timestamp": "2025-04-03T17:35:18-07:00",
          "tree_id": "d0c64cb663ef6d89d5c482fc687dba8eedf41898",
          "url": "https://github.com/iausathub/satchecker/commit/7768f23328bf31434be013f7878427f73e4919e7"
        },
        "date": 1743727004282,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 139047.14341955274,
            "unit": "iter/sec",
            "range": "stddev: 0.000001154009942724629",
            "extra": "mean: 7.191805422299532 usec\nrounds: 12319"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 191292.01624511555,
            "unit": "iter/sec",
            "range": "stddev: 7.450174938096846e-7",
            "extra": "mean: 5.227609701800788 usec\nrounds: 69411"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 758389.7677656717,
            "unit": "iter/sec",
            "range": "stddev: 4.4452368752988184e-7",
            "extra": "mean: 1.3185831909970882 usec\nrounds: 63216"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 692381.0050212279,
            "unit": "iter/sec",
            "range": "stddev: 4.0015790029586576e-7",
            "extra": "mean: 1.4442914995470462 usec\nrounds: 83043"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 330.5745006975558,
            "unit": "iter/sec",
            "range": "stddev: 0.004164658304286948",
            "extra": "mean: 3.0250367099999194 msec\nrounds: 300"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 217.4813321632226,
            "unit": "iter/sec",
            "range": "stddev: 0.0007539186462362539",
            "extra": "mean: 4.59809580000865 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 105796.03195407895,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029739427722748573",
            "extra": "mean: 9.452150345620266 usec\nrounds: 27929"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152002.47631080123,
            "unit": "iter/sec",
            "range": "stddev: 9.428173518520951e-7",
            "extra": "mean: 6.578840189124869 usec\nrounds: 42932"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11781071.301927337,
            "unit": "iter/sec",
            "range": "stddev: 1.1092876879400927e-8",
            "extra": "mean: 84.88192409433728 nsec\nrounds: 119833"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3634.384425433103,
            "unit": "iter/sec",
            "range": "stddev: 0.000050030820007113305",
            "extra": "mean: 275.1497593380843 usec\nrounds: 1205"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 137.53067516883607,
            "unit": "iter/sec",
            "range": "stddev: 0.002932981420707577",
            "extra": "mean: 7.2711051463419 msec\nrounds: 164"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156523.54437569078,
            "unit": "iter/sec",
            "range": "stddev: 0.000003152583635162956",
            "extra": "mean: 6.388815203416177 usec\nrounds: 10958"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16931.58815880919,
            "unit": "iter/sec",
            "range": "stddev: 0.000005502349945799724",
            "extra": "mean: 59.06120504589043 usec\nrounds: 8998"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 20.4708460752319,
            "unit": "iter/sec",
            "range": "stddev: 0.015617216694475751",
            "extra": "mean: 48.84995941667114 msec\nrounds: 12"
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
          "id": "13e370772ed71961d3cf77e4531209771ca9e577",
          "message": "Add missing line to codecov step",
          "timestamp": "2025-04-03T17:43:23-07:00",
          "tree_id": "857ded9d95a158b13cd2975e1b342f117240ff28",
          "url": "https://github.com/iausathub/satchecker/commit/13e370772ed71961d3cf77e4531209771ca9e577"
        },
        "date": 1743727507422,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 137609.61768566634,
            "unit": "iter/sec",
            "range": "stddev: 9.046620330390714e-7",
            "extra": "mean: 7.266933931058816 usec\nrounds: 12048"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 188620.06021743282,
            "unit": "iter/sec",
            "range": "stddev: 7.675901393013885e-7",
            "extra": "mean: 5.301663030153019 usec\nrounds: 65540"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 738830.3904783815,
            "unit": "iter/sec",
            "range": "stddev: 4.473432105930307e-7",
            "extra": "mean: 1.3534906155559128 usec\nrounds: 21365"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 682341.5067659222,
            "unit": "iter/sec",
            "range": "stddev: 4.020005708219257e-7",
            "extra": "mean: 1.465541799940731 usec\nrounds: 68134"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 331.45360728184346,
            "unit": "iter/sec",
            "range": "stddev: 0.004310788859282264",
            "extra": "mean: 3.0170134764883536 msec\nrounds: 319"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 231.8709280276081,
            "unit": "iter/sec",
            "range": "stddev: 0.00017452065723515823",
            "extra": "mean: 4.312744200001362 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104798.23686396895,
            "unit": "iter/sec",
            "range": "stddev: 0.0000034060415964907825",
            "extra": "mean: 9.542145268131065 usec\nrounds: 26427"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152908.49728017478,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010266896773844316",
            "extra": "mean: 6.539858920774668 usec\nrounds: 39375"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12049461.997830298,
            "unit": "iter/sec",
            "range": "stddev: 1.1272125059248451e-8",
            "extra": "mean: 82.99125721800782 nsec\nrounds: 118977"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 2910.777672621276,
            "unit": "iter/sec",
            "range": "stddev: 0.00024053573835868745",
            "extra": "mean: 343.55080066951956 usec\nrounds: 1194"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 141.81240813572097,
            "unit": "iter/sec",
            "range": "stddev: 0.0009231291850199974",
            "extra": "mean: 7.05156913380213 msec\nrounds: 142"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 147799.19945975285,
            "unit": "iter/sec",
            "range": "stddev: 0.000001563859479114237",
            "extra": "mean: 6.765936511532389 usec\nrounds: 8978"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16656.663116672295,
            "unit": "iter/sec",
            "range": "stddev: 0.00000836173837883636",
            "extra": "mean: 60.03603440830003 usec\nrounds: 8341"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.50314569389341,
            "unit": "iter/sec",
            "range": "stddev: 0.025680387016867496",
            "extra": "mean: 54.04486440000469 msec\nrounds: 85"
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
          "id": "9f1fe13d0e6b029409a0a71b7697e797b664405b",
          "message": "Temporarily disable using the FOV result cache",
          "timestamp": "2025-04-25T10:11:54-07:00",
          "tree_id": "e0e2d2000ec1ffde06e9f5f537cb2983fc1a333e",
          "url": "https://github.com/iausathub/satchecker/commit/9f1fe13d0e6b029409a0a71b7697e797b664405b"
        },
        "date": 1745601202231,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 134155.7550702971,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010927950032240744",
            "extra": "mean: 7.454022374783726 usec\nrounds: 10771"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 185177.07982681392,
            "unit": "iter/sec",
            "range": "stddev: 9.751507379711416e-7",
            "extra": "mean: 5.400236362595445 usec\nrounds: 34574"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 762602.8028657334,
            "unit": "iter/sec",
            "range": "stddev: 4.5028565846278303e-7",
            "extra": "mean: 1.3112986160582778 usec\nrounds: 40460"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 681566.0812422737,
            "unit": "iter/sec",
            "range": "stddev: 5.168220561063469e-7",
            "extra": "mean: 1.4672091636035125 usec\nrounds: 32673"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 342.5861114344581,
            "unit": "iter/sec",
            "range": "stddev: 0.0006727704745794439",
            "extra": "mean: 2.9189741399990035 msec\nrounds: 300"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.89366540811596,
            "unit": "iter/sec",
            "range": "stddev: 0.0007210063313041142",
            "extra": "mean: 4.610554199996386 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104387.95957911076,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029857848460588194",
            "extra": "mean: 9.579648879353243 usec\nrounds: 26817"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 150695.15144129208,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010579282304194452",
            "extra": "mean: 6.635913567461928 usec\nrounds: 28716"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11751447.157442272,
            "unit": "iter/sec",
            "range": "stddev: 9.603252679358066e-9",
            "extra": "mean: 85.09590236858081 nsec\nrounds: 70592"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3565.9753287878766,
            "unit": "iter/sec",
            "range": "stddev: 0.000049905353794894766",
            "extra": "mean: 280.42818802672804 usec\nrounds: 1186"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.15588142846107,
            "unit": "iter/sec",
            "range": "stddev: 0.0005025835064009719",
            "extra": "mean: 6.7496476708071995 msec\nrounds: 161"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 151159.18364660107,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017644175580001338",
            "extra": "mean: 6.61554247565881 usec\nrounds: 10559"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16803.083331017035,
            "unit": "iter/sec",
            "range": "stddev: 0.000005104940205052309",
            "extra": "mean: 59.51288702794724 usec\nrounds: 8657"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 16.07071564250538,
            "unit": "iter/sec",
            "range": "stddev: 0.031010238906551777",
            "extra": "mean: 62.22498252380893 msec\nrounds: 21"
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
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "9f1fe13d0e6b029409a0a71b7697e797b664405b",
          "message": "Temporarily disable using the FOV result cache",
          "timestamp": "2025-04-25T17:11:54Z",
          "url": "https://github.com/iausathub/satchecker/commit/9f1fe13d0e6b029409a0a71b7697e797b664405b"
        },
        "date": 1745601949600,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 136207.7039585468,
            "unit": "iter/sec",
            "range": "stddev: 9.489049956042219e-7",
            "extra": "mean: 7.3417286316223205 usec\nrounds: 10167"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 185858.9929754713,
            "unit": "iter/sec",
            "range": "stddev: 8.320818388431677e-7",
            "extra": "mean: 5.380422996975857 usec\nrounds: 63452"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 697045.1593200369,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010259961915316284",
            "extra": "mean: 1.434627278633559 usec\nrounds: 44819"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 706402.2596380977,
            "unit": "iter/sec",
            "range": "stddev: 5.053870370425223e-7",
            "extra": "mean: 1.4156240107616835 usec\nrounds: 62422"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 360.04224056730214,
            "unit": "iter/sec",
            "range": "stddev: 0.00017902405636355484",
            "extra": "mean: 2.777451885713036 msec\nrounds: 315"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.22805382614115,
            "unit": "iter/sec",
            "range": "stddev: 0.0007196864361596387",
            "extra": "mean: 4.6247467999876335 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104592.15987952589,
            "unit": "iter/sec",
            "range": "stddev: 0.000002899943857043625",
            "extra": "mean: 9.5609460704497 usec\nrounds: 25626"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 142103.98987485882,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020830241050315654",
            "extra": "mean: 7.037100090438214 usec\nrounds: 35408"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11132004.735729925,
            "unit": "iter/sec",
            "range": "stddev: 2.1662186739446524e-8",
            "extra": "mean: 89.83107928350212 nsec\nrounds: 117717"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3584.0306588547405,
            "unit": "iter/sec",
            "range": "stddev: 0.000049117523595080166",
            "extra": "mean: 279.0154703418595 usec\nrounds: 1197"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 146.330035670269,
            "unit": "iter/sec",
            "range": "stddev: 0.00029590365293811756",
            "extra": "mean: 6.833866987180524 msec\nrounds: 156"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 152815.01137062718,
            "unit": "iter/sec",
            "range": "stddev: 0.000001683790784822135",
            "extra": "mean: 6.54385973623146 usec\nrounds: 9860"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16493.62066789579,
            "unit": "iter/sec",
            "range": "stddev: 0.000007659929702294014",
            "extra": "mean: 60.62950155913688 usec\nrounds: 7056"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.144645247099323,
            "unit": "iter/sec",
            "range": "stddev: 0.02041495533937427",
            "extra": "mean: 55.11267850000342 msec\nrounds: 24"
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
          "id": "1a0995927720c22f5a6602d8dc1a6dd418e28583",
          "message": "Update load test URLs and accept 429 errors",
          "timestamp": "2025-05-08T15:48:58-07:00",
          "tree_id": "432aec2272b5c587562e94cc7c27c07e043837c6",
          "url": "https://github.com/iausathub/satchecker/commit/1a0995927720c22f5a6602d8dc1a6dd418e28583"
        },
        "date": 1746744639117,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 136129.75752176924,
            "unit": "iter/sec",
            "range": "stddev: 8.999791860456637e-7",
            "extra": "mean: 7.345932426567972 usec\nrounds: 11765"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 184849.87109127638,
            "unit": "iter/sec",
            "range": "stddev: 9.735160475347924e-7",
            "extra": "mean: 5.409795495644211 usec\nrounds: 48620"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 757162.0863874765,
            "unit": "iter/sec",
            "range": "stddev: 4.958138928911045e-7",
            "extra": "mean: 1.3207211744728744 usec\nrounds: 45914"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 700750.3808107151,
            "unit": "iter/sec",
            "range": "stddev: 5.172414882325683e-7",
            "extra": "mean: 1.4270416790113987 usec\nrounds: 43739"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 353.2348798685635,
            "unit": "iter/sec",
            "range": "stddev: 0.00025073431353620217",
            "extra": "mean: 2.8309775081444215 msec\nrounds: 307"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 219.31034615892358,
            "unit": "iter/sec",
            "range": "stddev: 0.00037999436507611336",
            "extra": "mean: 4.5597483999927135 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104285.11467655345,
            "unit": "iter/sec",
            "range": "stddev: 0.000003461911992854476",
            "extra": "mean: 9.58909623009535 usec\nrounds: 24192"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152270.40723273472,
            "unit": "iter/sec",
            "range": "stddev: 9.969412705439357e-7",
            "extra": "mean: 6.567264238490999 usec\nrounds: 31850"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11867933.161711171,
            "unit": "iter/sec",
            "range": "stddev: 9.372621532659019e-9",
            "extra": "mean: 84.2606700234751 nsec\nrounds: 117578"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3625.987874762146,
            "unit": "iter/sec",
            "range": "stddev: 0.00004889679798320545",
            "extra": "mean: 275.7869122950658 usec\nrounds: 1220"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 146.9279466130733,
            "unit": "iter/sec",
            "range": "stddev: 0.00023774885178277482",
            "extra": "mean: 6.8060571392414895 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157727.4408151699,
            "unit": "iter/sec",
            "range": "stddev: 0.000003250269668870443",
            "extra": "mean: 6.340050880378084 usec\nrounds: 10790"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16069.275506901928,
            "unit": "iter/sec",
            "range": "stddev: 0.000007534643969574869",
            "extra": "mean: 62.23055915436195 usec\nrounds: 7379"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 18.793599532844926,
            "unit": "iter/sec",
            "range": "stddev: 0.02622441811792838",
            "extra": "mean: 53.20960459183641 msec\nrounds: 49"
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
          "id": "a65cc133aa2f8cd758c979cba46c16541cbfcf7a",
          "message": "Update loop syntax",
          "timestamp": "2025-05-08T15:56:26-07:00",
          "tree_id": "b37eeb86eab74884278930517a5ece31eaf3529a",
          "url": "https://github.com/iausathub/satchecker/commit/a65cc133aa2f8cd758c979cba46c16541cbfcf7a"
        },
        "date": 1746745074067,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138731.3484802972,
            "unit": "iter/sec",
            "range": "stddev: 9.333670377569295e-7",
            "extra": "mean: 7.208176168935756 usec\nrounds: 11892"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186743.54251341216,
            "unit": "iter/sec",
            "range": "stddev: 0.000001018374292850409",
            "extra": "mean: 5.354937507026133 usec\nrounds: 62151"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 752038.769324664,
            "unit": "iter/sec",
            "range": "stddev: 8.248591744315094e-7",
            "extra": "mean: 1.3297186804584649 usec\nrounds: 61958"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 617755.7885067998,
            "unit": "iter/sec",
            "range": "stddev: 0.00000420251155997859",
            "extra": "mean: 1.6187626544417117 usec\nrounds: 71398"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 341.7373226991101,
            "unit": "iter/sec",
            "range": "stddev: 0.0005080447192016671",
            "extra": "mean: 2.926224130574322 msec\nrounds: 314"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 217.7803642337374,
            "unit": "iter/sec",
            "range": "stddev: 0.0007042284170479815",
            "extra": "mean: 4.59178220000922 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 101584.8139966205,
            "unit": "iter/sec",
            "range": "stddev: 0.000014645477805443968",
            "extra": "mean: 9.843991051982119 usec\nrounds: 23692"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 149109.4978760712,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010319092354542332",
            "extra": "mean: 6.706480903256251 usec\nrounds: 34194"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11602670.23136208,
            "unit": "iter/sec",
            "range": "stddev: 1.1565246454248297e-8",
            "extra": "mean: 86.18705694977236 nsec\nrounds: 68181"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3671.2232122179257,
            "unit": "iter/sec",
            "range": "stddev: 0.00005040417468166869",
            "extra": "mean: 272.3887767630075 usec\nrounds: 1205"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 146.07802951387333,
            "unit": "iter/sec",
            "range": "stddev: 0.0005316408833109729",
            "extra": "mean: 6.845656416148658 msec\nrounds: 161"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 133837.95305627427,
            "unit": "iter/sec",
            "range": "stddev: 0.00004760995672165147",
            "extra": "mean: 7.471722162244474 usec\nrounds: 10103"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 14573.109507823661,
            "unit": "iter/sec",
            "range": "stddev: 0.000018633932709286178",
            "extra": "mean: 68.61953514197805 usec\nrounds: 6118"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 17.6061664082188,
            "unit": "iter/sec",
            "range": "stddev: 0.028514145593661278",
            "extra": "mean: 56.79828173912899 msec\nrounds: 23"
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
          "id": "89ba741272c1d3b2264f94c8095cf75df8f3b8b6",
          "message": "Increase timeout for load testing",
          "timestamp": "2025-05-09T13:40:40-07:00",
          "tree_id": "05b962bf67bb21a910138a377e751942dfdf5700",
          "url": "https://github.com/iausathub/satchecker/commit/89ba741272c1d3b2264f94c8095cf75df8f3b8b6"
        },
        "date": 1746823328994,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 134262.42080189017,
            "unit": "iter/sec",
            "range": "stddev: 8.715444018359422e-7",
            "extra": "mean: 7.448100473888683 usec\nrounds: 11814"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 181962.59218734765,
            "unit": "iter/sec",
            "range": "stddev: 8.18464706650126e-7",
            "extra": "mean: 5.4956350532224 usec\nrounds: 61535"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 748309.8797981349,
            "unit": "iter/sec",
            "range": "stddev: 4.5123283001477945e-7",
            "extra": "mean: 1.3363447777406887 usec\nrounds: 50592"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 702005.1513823469,
            "unit": "iter/sec",
            "range": "stddev: 5.623497488850928e-7",
            "extra": "mean: 1.4244909713708787 usec\nrounds: 45577"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 358.3411377001395,
            "unit": "iter/sec",
            "range": "stddev: 0.0002136853416793005",
            "extra": "mean: 2.790636895384313 msec\nrounds: 325"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 230.24680431192456,
            "unit": "iter/sec",
            "range": "stddev: 0.00013645584394405581",
            "extra": "mean: 4.343165600010934 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 95211.68982799353,
            "unit": "iter/sec",
            "range": "stddev: 0.000016194824167327444",
            "extra": "mean: 10.502912003836597 usec\nrounds: 17103"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 149877.54814040515,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011634028201603853",
            "extra": "mean: 6.672113417969721 usec\nrounds: 17484"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11399428.640467562,
            "unit": "iter/sec",
            "range": "stddev: 1.868454623654136e-8",
            "extra": "mean: 87.7236948919737 nsec\nrounds: 68933"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3438.9668205176863,
            "unit": "iter/sec",
            "range": "stddev: 0.00006507662715760588",
            "extra": "mean: 290.7850096237523 usec\nrounds: 1143"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 145.8354218370772,
            "unit": "iter/sec",
            "range": "stddev: 0.00123848522530551",
            "extra": "mean: 6.8570446562507215 msec\nrounds: 160"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 154773.1080910038,
            "unit": "iter/sec",
            "range": "stddev: 0.000004212232079728648",
            "extra": "mean: 6.461070739834326 usec\nrounds: 10786"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16817.33314597541,
            "unit": "iter/sec",
            "range": "stddev: 0.000006051086879786839",
            "extra": "mean: 59.4624600297766 usec\nrounds: 8669"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_simple_random_sleep",
            "value": 14.980222966646183,
            "unit": "iter/sec",
            "range": "stddev: 0.022126055651985322",
            "extra": "mean: 66.75468063636458 msec\nrounds: 11"
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
          "id": "19257a678859050a6f2f0b15ae0b8eae0dad9c5b",
          "message": "Add full benchmarking tests",
          "timestamp": "2025-05-09T16:03:04-07:00",
          "tree_id": "c5e74efc609ba86bde8f61327ef428794e3b6dd0",
          "url": "https://github.com/iausathub/satchecker/commit/19257a678859050a6f2f0b15ae0b8eae0dad9c5b"
        },
        "date": 1746835090735,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 134897.60649433997,
            "unit": "iter/sec",
            "range": "stddev: 9.070980778790045e-7",
            "extra": "mean: 7.41302997130611 usec\nrounds: 11778"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186000.6474486969,
            "unit": "iter/sec",
            "range": "stddev: 7.620733927613338e-7",
            "extra": "mean: 5.376325371533033 usec\nrounds: 58235"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 749684.5154971222,
            "unit": "iter/sec",
            "range": "stddev: 4.472754777311716e-7",
            "extra": "mean: 1.3338944306951457 usec\nrounds: 54997"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 688426.1649006574,
            "unit": "iter/sec",
            "range": "stddev: 5.826239216589501e-7",
            "extra": "mean: 1.452588601341589 usec\nrounds: 59305"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 329.65605608923534,
            "unit": "iter/sec",
            "range": "stddev: 0.0041877581920213534",
            "extra": "mean: 3.033464671825437 msec\nrounds: 323"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 216.03274019279786,
            "unit": "iter/sec",
            "range": "stddev: 0.0007276508430774819",
            "extra": "mean: 4.62892800002237 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104338.93026634312,
            "unit": "iter/sec",
            "range": "stddev: 0.00000296943362907157",
            "extra": "mean: 9.58415039762558 usec\nrounds: 27414"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 148708.1305406657,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014203846670876333",
            "extra": "mean: 6.724581879714641 usec\nrounds: 37781"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 10942658.360725045,
            "unit": "iter/sec",
            "range": "stddev: 1.556096645477866e-8",
            "extra": "mean: 91.38547207041215 nsec\nrounds: 110534"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3437.086619588709,
            "unit": "iter/sec",
            "range": "stddev: 0.00007192426462421644",
            "extra": "mean: 290.9440787150318 usec\nrounds: 902"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 2.2317994439856017,
            "unit": "iter/sec",
            "range": "stddev: 0.6063370958493278",
            "extra": "mean: 448.0689349999011 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 6.905264006435861,
            "unit": "iter/sec",
            "range": "stddev: 0.010223914091113511",
            "extra": "mean: 144.81705537514244 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.2549557272658332,
            "unit": "iter/sec",
            "range": "stddev: 0.2835749753602789",
            "extra": "mean: 3.9222496028000022 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.3640936028077575,
            "unit": "iter/sec",
            "range": "stddev: 0.1687843473641972",
            "extra": "mean: 422.99509580007 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.772861528177348,
            "unit": "iter/sec",
            "range": "stddev: 0.1135242996642585",
            "extra": "mean: 360.6382756001949 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 149.1332706886901,
            "unit": "iter/sec",
            "range": "stddev: 0.00048238331133544844",
            "extra": "mean: 6.7054118466124235 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 159560.34837707062,
            "unit": "iter/sec",
            "range": "stddev: 0.00000342494783754965",
            "extra": "mean: 6.267221212357941 usec\nrounds: 10890"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16366.335509324808,
            "unit": "iter/sec",
            "range": "stddev: 0.000007229065031666925",
            "extra": "mean: 61.10103263068538 usec\nrounds: 9010"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.1261810136479966,
            "unit": "iter/sec",
            "range": "stddev: 0.32933438039584906",
            "extra": "mean: 7.925122576599915 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.15021196817603336,
            "unit": "iter/sec",
            "range": "stddev: 0.7146450228756414",
            "extra": "mean: 6.657259152799997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.3497568512719327,
            "unit": "iter/sec",
            "range": "stddev: 0.6269249250956921",
            "extra": "mean: 2.8591291246000763 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.610389746059415,
            "unit": "iter/sec",
            "range": "stddev: 0.07681419691429713",
            "extra": "mean: 1.6382975082000484 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.4184692037913809,
            "unit": "iter/sec",
            "range": "stddev: 0.4518122458235687",
            "extra": "mean: 2.3896621088000756 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.25426082660311966,
            "unit": "iter/sec",
            "range": "stddev: 0.7965361150666076",
            "extra": "mean: 3.9329692007999255 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.31005972598956794,
            "unit": "iter/sec",
            "range": "stddev: 0.8156489092478088",
            "extra": "mean: 3.2251850729999205 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.2666913059421674,
            "unit": "iter/sec",
            "range": "stddev: 0.47589602553097904",
            "extra": "mean: 3.7496535422000306 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.25463222330519936,
            "unit": "iter/sec",
            "range": "stddev: 0.6437288651680682",
            "extra": "mean: 3.9272327242000755 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.37383265023176476,
            "unit": "iter/sec",
            "range": "stddev: 0.34050745189204434",
            "extra": "mean: 2.6749937421999674 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.7702420540327082,
            "unit": "iter/sec",
            "range": "stddev: 0.09926524715150006",
            "extra": "mean: 1.2982931725999152 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 5.921743718552177,
            "unit": "iter/sec",
            "range": "stddev: 0.023866386598256212",
            "extra": "mean: 168.8691789999471 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.13790063471199934,
            "unit": "iter/sec",
            "range": "stddev: 0.8393958011354123",
            "extra": "mean: 7.251598240200019 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.1255302109020893,
            "unit": "iter/sec",
            "range": "stddev: 1.3748278070976043",
            "extra": "mean: 7.96620982960012 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.09292234356817371,
            "unit": "iter/sec",
            "range": "stddev: 1.623527967276403",
            "extra": "mean: 10.761674335799944 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.10199663657706662,
            "unit": "iter/sec",
            "range": "stddev: 0.8451790798942297",
            "extra": "mean: 9.804244861000097 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.07018806246379078,
            "unit": "iter/sec",
            "range": "stddev: 1.0788718463767102",
            "extra": "mean: 14.247437026999979 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.05069497639314077,
            "unit": "iter/sec",
            "range": "stddev: 2.751747385440054",
            "extra": "mean: 19.725820409599873 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.12674176360061795,
            "unit": "iter/sec",
            "range": "stddev: 0.09161271422392774",
            "extra": "mean: 7.890059058600036 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.1535052755489172,
            "unit": "iter/sec",
            "range": "stddev: 1.381473981777293",
            "extra": "mean: 6.514434089799943 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.1257065861709427,
            "unit": "iter/sec",
            "range": "stddev: 0.2877480225761442",
            "extra": "mean: 7.955032671399931 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.15097687597877998,
            "unit": "iter/sec",
            "range": "stddev: 1.2827784828340743",
            "extra": "mean: 6.623530878599922 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.16979903492376172,
            "unit": "iter/sec",
            "range": "stddev: 1.5257246948930179",
            "extra": "mean: 5.8893149801999245 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.11466707482158162,
            "unit": "iter/sec",
            "range": "stddev: 0.24378503142860455",
            "extra": "mean: 8.720899190599994 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.24242743192296262,
            "unit": "iter/sec",
            "range": "stddev: 0.07327884849636034",
            "extra": "mean: 4.12494572939986 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.2735932450024049,
            "unit": "iter/sec",
            "range": "stddev: 0.052136493749095965",
            "extra": "mean: 3.6550610011998286 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.4656976106967982,
            "unit": "iter/sec",
            "range": "stddev: 0.05245113931183234",
            "extra": "mean: 2.1473161490001074 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.5826737504255465,
            "unit": "iter/sec",
            "range": "stddev: 0.015843884111408472",
            "extra": "mean: 1.7162262745999215 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.5601794180104855,
            "unit": "iter/sec",
            "range": "stddev: 0.05170128644721334",
            "extra": "mean: 1.7851423451999835 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.33317063158769455,
            "unit": "iter/sec",
            "range": "stddev: 0.07258473232763074",
            "extra": "mean: 3.0014650307999546 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.37288248035868543,
            "unit": "iter/sec",
            "range": "stddev: 0.03710726116269018",
            "extra": "mean: 2.6818100948000394 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.40377392590903965,
            "unit": "iter/sec",
            "range": "stddev: 0.11488362247732782",
            "extra": "mean: 2.4766334224000275 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.39992519872669174,
            "unit": "iter/sec",
            "range": "stddev: 0.030957522783827827",
            "extra": "mean: 2.500467595400005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.624337408735836,
            "unit": "iter/sec",
            "range": "stddev: 0.04031461320162687",
            "extra": "mean: 1.6016980338000395 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 1.3697570552972398,
            "unit": "iter/sec",
            "range": "stddev: 0.05655662866396218",
            "extra": "mean: 730.0564696000038 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 7.631850229523509,
            "unit": "iter/sec",
            "range": "stddev: 0.006378550536199394",
            "extra": "mean: 131.02982499991154 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.9668645507540355,
            "unit": "iter/sec",
            "range": "stddev: 0.03948681492384581",
            "extra": "mean: 1.0342710354000701 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 7.070466668595759,
            "unit": "iter/sec",
            "range": "stddev: 0.012883276334875886",
            "extra": "mean: 141.43338012490858 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.5081509499094734,
            "unit": "iter/sec",
            "range": "stddev: 0.024306827460830353",
            "extra": "mean: 663.0636011998831 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 137730.07517604163,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011865224532031088",
            "extra": "mean: 7.26057833571815 usec\nrounds: 17642"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186817.41161361613,
            "unit": "iter/sec",
            "range": "stddev: 8.045075960106086e-7",
            "extra": "mean: 5.352820121864462 usec\nrounds: 68363"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 752043.4730520375,
            "unit": "iter/sec",
            "range": "stddev: 3.653192299200518e-7",
            "extra": "mean: 1.3297103636066063 usec\nrounds: 64940"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 701398.2297213176,
            "unit": "iter/sec",
            "range": "stddev: 3.8610624328831555e-7",
            "extra": "mean: 1.4257235870089435 usec\nrounds: 68933"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 359.1326294301775,
            "unit": "iter/sec",
            "range": "stddev: 0.000339927738356606",
            "extra": "mean: 2.78448661595206 msec\nrounds: 401"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 229.60586774159694,
            "unit": "iter/sec",
            "range": "stddev: 0.0003280580415858208",
            "extra": "mean: 4.355289391495082 msec\nrounds: 212"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 107375.3470693139,
            "unit": "iter/sec",
            "range": "stddev: 0.000002964122279516333",
            "extra": "mean: 9.31312472829048 usec\nrounds: 29929"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152755.35230075053,
            "unit": "iter/sec",
            "range": "stddev: 9.734310929196122e-7",
            "extra": "mean: 6.546415460658701 usec\nrounds: 41212"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 10619846.709943349,
            "unit": "iter/sec",
            "range": "stddev: 1.1467325186041872e-8",
            "extra": "mean: 94.16331773072636 nsec\nrounds: 104855"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3676.083738002997,
            "unit": "iter/sec",
            "range": "stddev: 0.00004767998350566005",
            "extra": "mean: 272.02862373946954 usec\nrounds: 1289"
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
          "id": "19257a678859050a6f2f0b15ae0b8eae0dad9c5b",
          "message": "Add full benchmarking tests",
          "timestamp": "2025-05-09T23:03:04Z",
          "url": "https://github.com/iausathub/satchecker/commit/19257a678859050a6f2f0b15ae0b8eae0dad9c5b"
        },
        "date": 1746836351462,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 135578.43412494822,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011292535057150416",
            "extra": "mean: 7.375804319132395 usec\nrounds: 11253"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 183185.25247030964,
            "unit": "iter/sec",
            "range": "stddev: 9.15063321744579e-7",
            "extra": "mean: 5.458954727603294 usec\nrounds: 30703"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 763550.2316366512,
            "unit": "iter/sec",
            "range": "stddev: 5.181972163230383e-7",
            "extra": "mean: 1.3096715298697827 usec\nrounds: 41331"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 640400.17532911,
            "unit": "iter/sec",
            "range": "stddev: 5.730741972147561e-7",
            "extra": "mean: 1.5615236199554237 usec\nrounds: 47735"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 316.6876157892665,
            "unit": "iter/sec",
            "range": "stddev: 0.0051302659757083",
            "extra": "mean: 3.1576858397438254 msec\nrounds: 312"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 209.98540223475297,
            "unit": "iter/sec",
            "range": "stddev: 0.0007820880178210513",
            "extra": "mean: 4.7622358000012355 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 89929.5743106409,
            "unit": "iter/sec",
            "range": "stddev: 0.000029759869165268503",
            "extra": "mean: 11.119812449525574 usec\nrounds: 12370"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 151461.1424644968,
            "unit": "iter/sec",
            "range": "stddev: 0.000001039176527622624",
            "extra": "mean: 6.602353473164937 usec\nrounds: 32953"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11222923.31124972,
            "unit": "iter/sec",
            "range": "stddev: 1.1986055246777348e-8",
            "extra": "mean: 89.10334431299519 nsec\nrounds: 69219"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3544.1448793001537,
            "unit": "iter/sec",
            "range": "stddev: 0.000051519827065438054",
            "extra": "mean: 282.1555083260212 usec\nrounds: 1141"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 2.709167648037792,
            "unit": "iter/sec",
            "range": "stddev: 0.053458852645797264",
            "extra": "mean: 369.1170610000029 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 2.7235479332972883,
            "unit": "iter/sec",
            "range": "stddev: 0.06138295868899992",
            "extra": "mean: 367.16812939999954 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 3.25187840984166,
            "unit": "iter/sec",
            "range": "stddev: 0.04199869182155939",
            "extra": "mean: 307.51457279999954 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.6077364034656308,
            "unit": "iter/sec",
            "range": "stddev: 0.30425906024054156",
            "extra": "mean: 1.6454502219999938 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 1.9536876154805667,
            "unit": "iter/sec",
            "range": "stddev: 0.1549468183718832",
            "extra": "mean: 511.85255619999447 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 2.4162569171340618,
            "unit": "iter/sec",
            "range": "stddev: 0.05275735025609307",
            "extra": "mean: 413.8632745999985 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 2.781423805628159,
            "unit": "iter/sec",
            "range": "stddev: 0.04979081956511839",
            "extra": "mean: 359.5280941999988 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 3.445903884823922,
            "unit": "iter/sec",
            "range": "stddev: 0.008638692630596034",
            "extra": "mean: 290.1996206000092 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 3.328463897162697,
            "unit": "iter/sec",
            "range": "stddev: 0.0138390735664138",
            "extra": "mean: 300.43889039999385 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.7155693148918892,
            "unit": "iter/sec",
            "range": "stddev: 0.18304184510617513",
            "extra": "mean: 1.3974886558000095 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.208388574866855,
            "unit": "iter/sec",
            "range": "stddev: 0.10241853090473714",
            "extra": "mean: 452.81886140001006 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 2.5788801198328706,
            "unit": "iter/sec",
            "range": "stddev: 0.02953516559312976",
            "extra": "mean: 387.7652133999959 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 3.0062778940838935,
            "unit": "iter/sec",
            "range": "stddev: 0.021387616327862242",
            "extra": "mean: 332.6372461999995 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 3.198460254069191,
            "unit": "iter/sec",
            "range": "stddev: 0.008587486767192988",
            "extra": "mean: 312.65043819999505 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 3.3953988290402077,
            "unit": "iter/sec",
            "range": "stddev: 0.010029673392440909",
            "extra": "mean: 294.5162116000006 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.7379174100245632,
            "unit": "iter/sec",
            "range": "stddev: 0.19660113464086676",
            "extra": "mean: 1.355165207399989 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.03514001616986,
            "unit": "iter/sec",
            "range": "stddev: 0.11884342343424877",
            "extra": "mean: 491.3666833999969 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.669324509521793,
            "unit": "iter/sec",
            "range": "stddev: 0.05418562495092988",
            "extra": "mean: 374.6266129999867 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 136.58248565348492,
            "unit": "iter/sec",
            "range": "stddev: 0.0017448123189559219",
            "extra": "mean: 7.321582962965244 msec\nrounds: 162"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 150807.2600414683,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017082743309507886",
            "extra": "mean: 6.630980496065139 usec\nrounds: 9434"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16414.536629595732,
            "unit": "iter/sec",
            "range": "stddev: 0.000007007476620185458",
            "extra": "mean: 60.92161006829644 usec\nrounds: 8681"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.29016018703586055,
            "unit": "iter/sec",
            "range": "stddev: 0.14073087885358226",
            "extra": "mean: 3.4463721925999833 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.31307105390993833,
            "unit": "iter/sec",
            "range": "stddev: 0.1071998185240865",
            "extra": "mean: 3.1941630741999916 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.57238333240438,
            "unit": "iter/sec",
            "range": "stddev: 0.057079168191739804",
            "extra": "mean: 1.7470809217999999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.6112696908441637,
            "unit": "iter/sec",
            "range": "stddev: 0.05227072481157084",
            "extra": "mean: 1.6359391197999684 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.5723190707307088,
            "unit": "iter/sec",
            "range": "stddev: 0.07005651442486929",
            "extra": "mean: 1.7472770891999971 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.2891696230291769,
            "unit": "iter/sec",
            "range": "stddev: 0.11376084585192814",
            "extra": "mean: 3.458177900999999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.3157976873493652,
            "unit": "iter/sec",
            "range": "stddev: 0.057536020097136736",
            "extra": "mean: 3.166584304000003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.34308500630471644,
            "unit": "iter/sec",
            "range": "stddev: 0.07266793412284521",
            "extra": "mean: 2.9147295324000084 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.33323392927456674,
            "unit": "iter/sec",
            "range": "stddev: 0.18024983825150048",
            "extra": "mean: 3.0008949033999897 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.5364971370675272,
            "unit": "iter/sec",
            "range": "stddev: 0.08069263820771849",
            "extra": "mean: 1.8639428449999969 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 1.089260604860325,
            "unit": "iter/sec",
            "range": "stddev: 0.05385279712881996",
            "extra": "mean: 918.053949199998 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 3.140300734567877,
            "unit": "iter/sec",
            "range": "stddev: 0.006818821586105504",
            "extra": "mean: 318.4408387999838 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.30403058329155,
            "unit": "iter/sec",
            "range": "stddev: 0.30926142807369983",
            "extra": "mean: 3.289142786800005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.2741307092109634,
            "unit": "iter/sec",
            "range": "stddev: 0.09412643087126532",
            "extra": "mean: 3.6478948414000114 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.19311833001379555,
            "unit": "iter/sec",
            "range": "stddev: 0.11186236031523303",
            "extra": "mean: 5.178172366800004 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.17819915824683719,
            "unit": "iter/sec",
            "range": "stddev: 0.24031076707345453",
            "extra": "mean: 5.6116987860000105 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.1689590067264945,
            "unit": "iter/sec",
            "range": "stddev: 0.12120390823439361",
            "extra": "mean: 5.918595400000004 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.10919486364460483,
            "unit": "iter/sec",
            "range": "stddev: 0.10419579574494403",
            "extra": "mean: 9.157939912399979 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.33773890918217675,
            "unit": "iter/sec",
            "range": "stddev: 0.09709913336765148",
            "extra": "mean: 2.960867027199993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.34625141198711923,
            "unit": "iter/sec",
            "range": "stddev: 0.12761875617417778",
            "extra": "mean: 2.888074865199974 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.3280996870260952,
            "unit": "iter/sec",
            "range": "stddev: 0.18061007636012738",
            "extra": "mean: 3.0478541722000045 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.31145967960579235,
            "unit": "iter/sec",
            "range": "stddev: 0.13497767096638624",
            "extra": "mean: 3.2106884630000194 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.24512905694534395,
            "unit": "iter/sec",
            "range": "stddev: 0.17249632244058571",
            "extra": "mean: 4.079483731799973 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.12575243222107535,
            "unit": "iter/sec",
            "range": "stddev: 0.17896337405880064",
            "extra": "mean: 7.952132474400014 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.2719765035599491,
            "unit": "iter/sec",
            "range": "stddev: 0.1206351366927188",
            "extra": "mean: 3.676788203800038 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.2835900729251654,
            "unit": "iter/sec",
            "range": "stddev: 0.09590203271560731",
            "extra": "mean: 3.526216519799982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.4783528136846673,
            "unit": "iter/sec",
            "range": "stddev: 0.07087119112729776",
            "extra": "mean: 2.090507197599982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.4847772551925039,
            "unit": "iter/sec",
            "range": "stddev: 0.12416901486894476",
            "extra": "mean: 2.062803048800015 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.4715835979396086,
            "unit": "iter/sec",
            "range": "stddev: 0.08796041649213354",
            "extra": "mean: 2.120514802400021 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.2697902951644323,
            "unit": "iter/sec",
            "range": "stddev: 0.11071157578072306",
            "extra": "mean: 3.706582549199993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.2871888276040573,
            "unit": "iter/sec",
            "range": "stddev: 0.09637037286508061",
            "extra": "mean: 3.4820296051999775 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.30936995828344777,
            "unit": "iter/sec",
            "range": "stddev: 0.03917188764031687",
            "extra": "mean: 3.2323759085999884 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.3032773761608512,
            "unit": "iter/sec",
            "range": "stddev: 0.11101347306075408",
            "extra": "mean: 3.297311565600012 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.4425526678203642,
            "unit": "iter/sec",
            "range": "stddev: 0.10454232353630605",
            "extra": "mean: 2.2596180584000196 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.9250105952240337,
            "unit": "iter/sec",
            "range": "stddev: 0.051398066882581354",
            "extra": "mean: 1.0810686981999424 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 3.031293204983877,
            "unit": "iter/sec",
            "range": "stddev: 0.014837447171392446",
            "extra": "mean: 329.89220520003073 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.5339941308211937,
            "unit": "iter/sec",
            "range": "stddev: 0.11207402439656196",
            "extra": "mean: 1.8726797585999067 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 2.0761345021727777,
            "unit": "iter/sec",
            "range": "stddev: 0.03510321334348636",
            "extra": "mean: 481.66436179999437 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.016617557396706,
            "unit": "iter/sec",
            "range": "stddev: 0.14965991316459168",
            "extra": "mean: 983.6540720000357 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 136954.99261101292,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011396068466426743",
            "extra": "mean: 7.301668825175691 usec\nrounds: 17770"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 187823.42929934416,
            "unit": "iter/sec",
            "range": "stddev: 8.203231091643483e-7",
            "extra": "mean: 5.324149408465155 usec\nrounds: 48953"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 760553.4324919863,
            "unit": "iter/sec",
            "range": "stddev: 4.44252235660044e-7",
            "extra": "mean: 1.3148320121617973 usec\nrounds: 46795"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 711939.8757346545,
            "unit": "iter/sec",
            "range": "stddev: 3.6343536295887474e-7",
            "extra": "mean: 1.4046129934330407 usec\nrounds: 66278"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 359.6384584130922,
            "unit": "iter/sec",
            "range": "stddev: 0.00018653860865261717",
            "extra": "mean: 2.7805702549513436 msec\nrounds: 404"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 217.85359956251668,
            "unit": "iter/sec",
            "range": "stddev: 0.0007234703205556011",
            "extra": "mean: 4.590238591458451 msec\nrounds: 164"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 106273.84476495499,
            "unit": "iter/sec",
            "range": "stddev: 0.000012044958041188501",
            "extra": "mean: 9.409652979166152 usec\nrounds: 29540"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 150078.48936640084,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010632531966314157",
            "extra": "mean: 6.663180074784769 usec\nrounds: 36818"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 10636159.770543104,
            "unit": "iter/sec",
            "range": "stddev: 9.895617200726488e-9",
            "extra": "mean: 94.01889606523949 nsec\nrounds: 106872"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3616.5821444554203,
            "unit": "iter/sec",
            "range": "stddev: 0.000048127112158827956",
            "extra": "mean: 276.5041578090793 usec\nrounds: 1242"
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
          "id": "19257a678859050a6f2f0b15ae0b8eae0dad9c5b",
          "message": "Add full benchmarking tests",
          "timestamp": "2025-05-09T23:03:04Z",
          "url": "https://github.com/iausathub/satchecker/commit/19257a678859050a6f2f0b15ae0b8eae0dad9c5b"
        },
        "date": 1747154943910,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 136883.47977067498,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010597819651869411",
            "extra": "mean: 7.305483478907243 usec\nrounds: 10199"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 185117.74545793966,
            "unit": "iter/sec",
            "range": "stddev: 9.096279101705035e-7",
            "extra": "mean: 5.401967258872049 usec\nrounds: 53175"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 751043.6958146031,
            "unit": "iter/sec",
            "range": "stddev: 4.771736714038411e-7",
            "extra": "mean: 1.331480452565908 usec\nrounds: 37217"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 697415.5260270963,
            "unit": "iter/sec",
            "range": "stddev: 5.005104011265929e-7",
            "extra": "mean: 1.4338654111941114 usec\nrounds: 48429"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 319.5186048618299,
            "unit": "iter/sec",
            "range": "stddev: 0.005346967629342454",
            "extra": "mean: 3.129708207233917 msec\nrounds: 304"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 166.17911376496525,
            "unit": "iter/sec",
            "range": "stddev: 0.002301309670791841",
            "extra": "mean: 6.017603399993732 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 80533.38760202618,
            "unit": "iter/sec",
            "range": "stddev: 0.00010198493654036389",
            "extra": "mean: 12.417210175507886 usec\nrounds: 17847"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 149086.9907246997,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013662852637168365",
            "extra": "mean: 6.707493357663749 usec\nrounds: 19947"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11883955.662193462,
            "unit": "iter/sec",
            "range": "stddev: 9.046287880071695e-9",
            "extra": "mean: 84.14706587817501 nsec\nrounds: 117565"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3567.6894907947667,
            "unit": "iter/sec",
            "range": "stddev: 0.00004894324967915267",
            "extra": "mean: 280.2934511481917 usec\nrounds: 1177"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 2.396471517393061,
            "unit": "iter/sec",
            "range": "stddev: 0.06930441677670132",
            "extra": "mean: 417.2801523999851 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 2.555643050096646,
            "unit": "iter/sec",
            "range": "stddev: 0.047883864256824824",
            "extra": "mean: 391.29095120000557 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 3.0696468992539288,
            "unit": "iter/sec",
            "range": "stddev: 0.04575030503538446",
            "extra": "mean: 325.7703679999963 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.6042155204496419,
            "unit": "iter/sec",
            "range": "stddev: 0.13294276167359295",
            "extra": "mean: 1.6550385849999771 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 1.7764551110979716,
            "unit": "iter/sec",
            "range": "stddev: 0.1875688624395823",
            "extra": "mean: 562.9188115999909 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 2.497052696240891,
            "unit": "iter/sec",
            "range": "stddev: 0.03274476535458388",
            "extra": "mean: 400.4721252000081 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 3.042452585285487,
            "unit": "iter/sec",
            "range": "stddev: 0.022886911907979337",
            "extra": "mean: 328.6821970000119 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 3.240500131505535,
            "unit": "iter/sec",
            "range": "stddev: 0.00908157994425174",
            "extra": "mean: 308.5943402000112 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 3.035270830477799,
            "unit": "iter/sec",
            "range": "stddev: 0.04764434785558131",
            "extra": "mean: 329.4598920000112 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.6016399880624521,
            "unit": "iter/sec",
            "range": "stddev: 0.050141457946395615",
            "extra": "mean: 1.6621235619999992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 1.679016068832935,
            "unit": "iter/sec",
            "range": "stddev: 0.2443223463320778",
            "extra": "mean: 595.5869145999827 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 2.0359953115149683,
            "unit": "iter/sec",
            "range": "stddev: 0.1604532521755794",
            "extra": "mean: 491.1602665999794 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 3.001607507899333,
            "unit": "iter/sec",
            "range": "stddev: 0.01957360175824506",
            "extra": "mean: 333.15481699999054 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 3.254650487087519,
            "unit": "iter/sec",
            "range": "stddev: 0.0033493230983600198",
            "extra": "mean: 307.2526539999899 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 3.227654512880782,
            "unit": "iter/sec",
            "range": "stddev: 0.007671745743030892",
            "extra": "mean: 309.8225030000094 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.6653009563789012,
            "unit": "iter/sec",
            "range": "stddev: 0.15899563430045996",
            "extra": "mean: 1.5030791560000125 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 1.9305673603368316,
            "unit": "iter/sec",
            "range": "stddev: 0.14462714643349844",
            "extra": "mean: 517.9824441999926 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.373847864630105,
            "unit": "iter/sec",
            "range": "stddev: 0.07094939774472138",
            "extra": "mean: 421.2569873999996 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.71967178086143,
            "unit": "iter/sec",
            "range": "stddev: 0.0001422289794553605",
            "extra": "mean: 6.724060025317302 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 149388.64511333048,
            "unit": "iter/sec",
            "range": "stddev: 0.0000036083605311705265",
            "extra": "mean: 6.693949190324148 usec\nrounds: 9073"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16707.35539700674,
            "unit": "iter/sec",
            "range": "stddev: 0.000006114761971010704",
            "extra": "mean: 59.85387730359516 usec\nrounds: 8900"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.2817668743306478,
            "unit": "iter/sec",
            "range": "stddev: 0.10876374255691607",
            "extra": "mean: 3.5490332296000133 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.2964276259605898,
            "unit": "iter/sec",
            "range": "stddev: 0.07128956883691875",
            "extra": "mean: 3.3735047357999974 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.5328516411335021,
            "unit": "iter/sec",
            "range": "stddev: 0.05889181053484698",
            "extra": "mean: 1.8766949799999906 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.5548423844579539,
            "unit": "iter/sec",
            "range": "stddev: 0.08624962537925648",
            "extra": "mean: 1.8023136443999987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.5552711379666032,
            "unit": "iter/sec",
            "range": "stddev: 0.08892420057198151",
            "extra": "mean: 1.8009219849999567 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.27669227567380283,
            "unit": "iter/sec",
            "range": "stddev: 0.1077626180103015",
            "extra": "mean: 3.614123298399977 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.2924829151071501,
            "unit": "iter/sec",
            "range": "stddev: 0.10215174036574645",
            "extra": "mean: 3.4190031223999995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.3182058180109512,
            "unit": "iter/sec",
            "range": "stddev: 0.15242614729314566",
            "extra": "mean: 3.1426201011999866 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.33517958455939284,
            "unit": "iter/sec",
            "range": "stddev: 0.10889379835468681",
            "extra": "mean: 2.983475265400011 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.4621728590320625,
            "unit": "iter/sec",
            "range": "stddev: 0.07869283009726115",
            "extra": "mean: 2.163692610800035 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.859029546878233,
            "unit": "iter/sec",
            "range": "stddev: 0.0681064647484523",
            "extra": "mean: 1.164104312400036 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 2.9586431581055717,
            "unit": "iter/sec",
            "range": "stddev: 0.011966286905250182",
            "extra": "mean: 337.9927711999926 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.24305826872723912,
            "unit": "iter/sec",
            "range": "stddev: 0.29630505996853285",
            "extra": "mean: 4.114239787999987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.21266300837944227,
            "unit": "iter/sec",
            "range": "stddev: 0.25692848064184626",
            "extra": "mean: 4.702275245799956 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.16297408192692467,
            "unit": "iter/sec",
            "range": "stddev: 0.08525830282307152",
            "extra": "mean: 6.135944980799991 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.12038583768748205,
            "unit": "iter/sec",
            "range": "stddev: 1.8415325679452925",
            "extra": "mean: 8.306624925400024 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.08928646705035166,
            "unit": "iter/sec",
            "range": "stddev: 0.19598067502863983",
            "extra": "mean: 11.19990557399999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.06010517788440868,
            "unit": "iter/sec",
            "range": "stddev: 0.2665809229289821",
            "extra": "mean: 16.63750171280003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.18667100940790954,
            "unit": "iter/sec",
            "range": "stddev: 0.06443836178440478",
            "extra": "mean: 5.357018227800017 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.1834054242332196,
            "unit": "iter/sec",
            "range": "stddev: 0.07844277289504842",
            "extra": "mean: 5.452401444399993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.17804631715325678,
            "unit": "iter/sec",
            "range": "stddev: 0.0857174142371594",
            "extra": "mean: 5.6165160616000325 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.1757406061123671,
            "unit": "iter/sec",
            "range": "stddev: 0.0910247882045649",
            "extra": "mean: 5.690204569799926 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.16080089775367581,
            "unit": "iter/sec",
            "range": "stddev: 0.1345539160720982",
            "extra": "mean: 6.218870752400017 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.08800063597777988,
            "unit": "iter/sec",
            "range": "stddev: 0.19209556239340658",
            "extra": "mean: 11.363554239000042 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.18060643007313965,
            "unit": "iter/sec",
            "range": "stddev: 0.13021779405710832",
            "extra": "mean: 5.536901424799953 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.20365194901841924,
            "unit": "iter/sec",
            "range": "stddev: 0.05647155637488709",
            "extra": "mean: 4.910338471199975 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.32704477911433316,
            "unit": "iter/sec",
            "range": "stddev: 0.0868689003693506",
            "extra": "mean: 3.0576852586000314 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.375294025042153,
            "unit": "iter/sec",
            "range": "stddev: 0.1022258086897548",
            "extra": "mean: 2.6645774600000096 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.40693518713194393,
            "unit": "iter/sec",
            "range": "stddev: 0.030603434611016125",
            "extra": "mean: 2.45739378559997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.23794702181314462,
            "unit": "iter/sec",
            "range": "stddev: 0.2883197088506915",
            "extra": "mean: 4.20261616380003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.2663357856888281,
            "unit": "iter/sec",
            "range": "stddev: 0.10629052994047035",
            "extra": "mean: 3.7546587944000294 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.3017555000877203,
            "unit": "iter/sec",
            "range": "stddev: 0.02856596049164661",
            "extra": "mean: 3.3139412528000323 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.3109631125297241,
            "unit": "iter/sec",
            "range": "stddev: 0.08098186331565238",
            "extra": "mean: 3.2158155090000036 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.4426418808380072,
            "unit": "iter/sec",
            "range": "stddev: 0.039793172990685285",
            "extra": "mean: 2.2591626397999334 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.8194819569252679,
            "unit": "iter/sec",
            "range": "stddev: 0.05304829395134887",
            "extra": "mean: 1.2202831210000569 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 3.020503367756201,
            "unit": "iter/sec",
            "range": "stddev: 0.013918881355118635",
            "extra": "mean: 331.07064559999344 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.4306687073605901,
            "unit": "iter/sec",
            "range": "stddev: 0.4655382562946981",
            "extra": "mean: 2.321970421600008 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 2.1536629068201267,
            "unit": "iter/sec",
            "range": "stddev: 0.004442691804295512",
            "extra": "mean: 464.32521860001543 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.0020950335895145,
            "unit": "iter/sec",
            "range": "stddev: 0.061746103752641376",
            "extra": "mean: 997.9093464000016 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 137525.16450014076,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010325819977679962",
            "extra": "mean: 7.271396501394306 usec\nrounds: 17667"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 184878.22493399307,
            "unit": "iter/sec",
            "range": "stddev: 7.551513377098278e-7",
            "extra": "mean: 5.408965822540915 usec\nrounds: 70191"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 748315.0467543484,
            "unit": "iter/sec",
            "range": "stddev: 3.4935980675864256e-7",
            "extra": "mean: 1.3363355505642704 usec\nrounds: 63296"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 715761.0036367823,
            "unit": "iter/sec",
            "range": "stddev: 4.2111977487469866e-7",
            "extra": "mean: 1.397114392819669 usec\nrounds: 81281"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 362.88752672460987,
            "unit": "iter/sec",
            "range": "stddev: 0.0001695995440746951",
            "extra": "mean: 2.755674765197663 msec\nrounds: 362"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 230.756501714464,
            "unit": "iter/sec",
            "range": "stddev: 0.00013600818560331488",
            "extra": "mean: 4.333572369880138 msec\nrounds: 219"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 105565.26970187126,
            "unit": "iter/sec",
            "range": "stddev: 0.000002839467213991774",
            "extra": "mean: 9.472812439395245 usec\nrounds: 26253"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152367.9368537783,
            "unit": "iter/sec",
            "range": "stddev: 8.814962279323579e-7",
            "extra": "mean: 6.563060579862428 usec\nrounds: 38643"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11196434.151825933,
            "unit": "iter/sec",
            "range": "stddev: 9.21716876612906e-9",
            "extra": "mean: 89.31415006241511 nsec\nrounds: 111285"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3649.147130906859,
            "unit": "iter/sec",
            "range": "stddev: 0.000049637978510792195",
            "extra": "mean: 274.0366348976144 usec\nrounds: 1301"
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
          "id": "44143d4dc41baeb4af8c817cabd2c9c7bce40017",
          "message": "Add threading and keep-alive to Gunicorn config",
          "timestamp": "2025-05-15T09:52:29-07:00",
          "tree_id": "1c9633d501214f5b43ac5744ad7440aa25cbad4c",
          "url": "https://github.com/iausathub/satchecker/commit/44143d4dc41baeb4af8c817cabd2c9c7bce40017"
        },
        "date": 1747332501325,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 134015.9365021323,
            "unit": "iter/sec",
            "range": "stddev: 9.716459133143131e-7",
            "extra": "mean: 7.461799141955698 usec\nrounds: 11889"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 184829.18144295036,
            "unit": "iter/sec",
            "range": "stddev: 9.84506235963886e-7",
            "extra": "mean: 5.41040106433984 usec\nrounds: 18416"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 736643.0001796248,
            "unit": "iter/sec",
            "range": "stddev: 3.99214205452062e-7",
            "extra": "mean: 1.3575096753191949 usec\nrounds: 49559"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 682509.2989346022,
            "unit": "iter/sec",
            "range": "stddev: 5.297479693616286e-7",
            "extra": "mean: 1.4651815023780645 usec\nrounds: 43173"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 326.29321233858565,
            "unit": "iter/sec",
            "range": "stddev: 0.00432719722440792",
            "extra": "mean: 3.064728171428608 msec\nrounds: 315"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 219.33663914573947,
            "unit": "iter/sec",
            "range": "stddev: 0.00041331160600504565",
            "extra": "mean: 4.5592018000036205 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 100165.10741239808,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032863861605378424",
            "extra": "mean: 9.983516474282975 usec\nrounds: 18969"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152901.4384117194,
            "unit": "iter/sec",
            "range": "stddev: 9.789980778777493e-7",
            "extra": "mean: 6.540160840784826 usec\nrounds: 31211"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 10558216.919086687,
            "unit": "iter/sec",
            "range": "stddev: 2.5055947683118386e-8",
            "extra": "mean: 94.71296220407113 nsec\nrounds: 68790"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3517.7427313201797,
            "unit": "iter/sec",
            "range": "stddev: 0.00005605714727136025",
            "extra": "mean: 284.27320483004974 usec\nrounds: 1118"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 2.894470526290081,
            "unit": "iter/sec",
            "range": "stddev: 0.06637180297555453",
            "extra": "mean: 345.48633019999215 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 3.7883807712915956,
            "unit": "iter/sec",
            "range": "stddev: 0.023713459871643746",
            "extra": "mean: 263.96501839994926 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 4.325432738675285,
            "unit": "iter/sec",
            "range": "stddev: 0.014064624724576816",
            "extra": "mean: 231.19074100000034 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 4.3065111305401995,
            "unit": "iter/sec",
            "range": "stddev: 0.02114091701614351",
            "extra": "mean: 232.20652859999973 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.6131311575001577,
            "unit": "iter/sec",
            "range": "stddev: 0.028309686578704574",
            "extra": "mean: 1.6309724074000314 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 1.961102783743344,
            "unit": "iter/sec",
            "range": "stddev: 0.17380867558953442",
            "extra": "mean: 509.917179400054 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.9854035310002818,
            "unit": "iter/sec",
            "range": "stddev: 0.0460146614217501",
            "extra": "mean: 334.96309280003516 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.15851598508502,
            "unit": "iter/sec",
            "range": "stddev: 0.0003037630399001101",
            "extra": "mean: 6.749527648486092 msec\nrounds: 165"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 149628.27041246023,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014863123502860976",
            "extra": "mean: 6.683229026462939 usec\nrounds: 8964"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16686.75292437297,
            "unit": "iter/sec",
            "range": "stddev: 0.00000544531305202785",
            "extra": "mean: 59.92777651423017 usec\nrounds: 6855"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.20320388611019577,
            "unit": "iter/sec",
            "range": "stddev: 0.035921706362031604",
            "extra": "mean: 4.921165727400057 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.22546544945003422,
            "unit": "iter/sec",
            "range": "stddev: 0.09555084720394852",
            "extra": "mean: 4.435269361399923 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.39705417345282296,
            "unit": "iter/sec",
            "range": "stddev: 0.09739532874759961",
            "extra": "mean: 2.5185480139999528 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.4712638442419763,
            "unit": "iter/sec",
            "range": "stddev: 0.06322440905688627",
            "extra": "mean: 2.121953576999931 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.11697919113775158,
            "unit": "iter/sec",
            "range": "stddev: 0.3095449383598184",
            "extra": "mean: 8.548528932999943 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.11457766421073018,
            "unit": "iter/sec",
            "range": "stddev: 0.2921986690584132",
            "extra": "mean: 8.727704538999934 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.11239811781384222,
            "unit": "iter/sec",
            "range": "stddev: 0.3334637880033119",
            "extra": "mean: 8.896946136199858 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.1634925421726395,
            "unit": "iter/sec",
            "range": "stddev: 0.10911332111794221",
            "extra": "mean: 6.116486946199984 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.070162348983604,
            "unit": "iter/sec",
            "range": "stddev: 3.5877647660060297",
            "extra": "mean: 14.252658505399904 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.14844718866717074,
            "unit": "iter/sec",
            "range": "stddev: 1.732158842394001",
            "extra": "mean: 6.736402413400174 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.16092139684403936,
            "unit": "iter/sec",
            "range": "stddev: 1.528625921168247",
            "extra": "mean: 6.214214017599988 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.2368116283930523,
            "unit": "iter/sec",
            "range": "stddev: 0.32262966552021605",
            "extra": "mean: 4.222765608199916 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.26799396913057444,
            "unit": "iter/sec",
            "range": "stddev: 0.4190960502773329",
            "extra": "mean: 3.731427252800495 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.2779092300941852,
            "unit": "iter/sec",
            "range": "stddev: 0.3975438947502137",
            "extra": "mean: 3.5982971838002413 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.16553995631088675,
            "unit": "iter/sec",
            "range": "stddev: 0.3515842738644147",
            "extra": "mean: 6.040837646 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.17589863448468993,
            "unit": "iter/sec",
            "range": "stddev: 0.30033278411932657",
            "extra": "mean: 5.685092456400161 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.20485200263099493,
            "unit": "iter/sec",
            "range": "stddev: 0.19338129432126472",
            "extra": "mean: 4.881572975399831 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.2066247394500858,
            "unit": "iter/sec",
            "range": "stddev: 0.10272109075239436",
            "extra": "mean: 4.839691523200054 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.3165061511893007,
            "unit": "iter/sec",
            "range": "stddev: 0.1257710854316063",
            "extra": "mean: 3.1594962569997733 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.6624501521048147,
            "unit": "iter/sec",
            "range": "stddev: 0.06754954116693353",
            "extra": "mean: 1.5095475438003632 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 3.6823312268661588,
            "unit": "iter/sec",
            "range": "stddev: 0.013316101536397104",
            "extra": "mean: 271.56709660011984 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.4305258485353585,
            "unit": "iter/sec",
            "range": "stddev: 0.1259249698950114",
            "extra": "mean: 2.322740907199841 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 2.6520113591118464,
            "unit": "iter/sec",
            "range": "stddev: 0.023530728693618268",
            "extra": "mean: 377.07229140032723 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.0170907341933388,
            "unit": "iter/sec",
            "range": "stddev: 0.11282695854565838",
            "extra": "mean: 983.1964507995508 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 137436.12197012253,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011338724799553774",
            "extra": "mean: 7.276107515732958 usec\nrounds: 15300"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186774.41128654228,
            "unit": "iter/sec",
            "range": "stddev: 8.994080960910772e-7",
            "extra": "mean: 5.354052480271709 usec\nrounds: 56421"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 737092.5862078179,
            "unit": "iter/sec",
            "range": "stddev: 3.5817620806085773e-7",
            "extra": "mean: 1.356681668913242 usec\nrounds: 63862"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 695772.9933556708,
            "unit": "iter/sec",
            "range": "stddev: 3.675662207500798e-7",
            "extra": "mean: 1.4372503813018969 usec\nrounds: 67577"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 361.8089820931288,
            "unit": "iter/sec",
            "range": "stddev: 0.0001301054747931063",
            "extra": "mean: 2.7638893711671377 msec\nrounds: 361"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 229.79594525568254,
            "unit": "iter/sec",
            "range": "stddev: 0.000320197212380505",
            "extra": "mean: 4.351686879798291 msec\nrounds: 158"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 101591.15052067049,
            "unit": "iter/sec",
            "range": "stddev: 0.0000044774550938065324",
            "extra": "mean: 9.843377054741914 usec\nrounds: 26068"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 150468.6465774285,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011218523337220223",
            "extra": "mean: 6.6459028026507685 usec\nrounds: 40053"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11065354.063502302,
            "unit": "iter/sec",
            "range": "stddev: 1.004062988138961e-8",
            "extra": "mean: 90.37216470988385 nsec\nrounds: 110412"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3615.5096047224124,
            "unit": "iter/sec",
            "range": "stddev: 0.00004759335705175486",
            "extra": "mean: 276.58618267639116 usec\nrounds: 1259"
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
          "id": "9e07554a1098e8ba02fb2f0af9b0f0f72867c2c3",
          "message": "Change rate limiting to moving window\n\nFixed window was causing Redis key lock issues and forcing requests from the same user to run sequentially even though multiple replicas were available.",
          "timestamp": "2025-05-15T10:20:29-07:00",
          "tree_id": "8a662de6aff8f20a8ee6d0d43cf9504c72dafb84",
          "url": "https://github.com/iausathub/satchecker/commit/9e07554a1098e8ba02fb2f0af9b0f0f72867c2c3"
        },
        "date": 1747333239652,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 127296.95905195356,
            "unit": "iter/sec",
            "range": "stddev: 0.000001418095813605989",
            "extra": "mean: 7.85564720043211 usec\nrounds: 8682"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 181694.78819144427,
            "unit": "iter/sec",
            "range": "stddev: 8.652001663505318e-7",
            "extra": "mean: 5.503735192152796 usec\nrounds: 38628"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 760493.0674920272,
            "unit": "iter/sec",
            "range": "stddev: 3.6579939669895606e-7",
            "extra": "mean: 1.314936378444349 usec\nrounds: 39782"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 678706.3342368201,
            "unit": "iter/sec",
            "range": "stddev: 4.58922194735253e-7",
            "extra": "mean: 1.473391288036913 usec\nrounds: 42332"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 331.4014992580583,
            "unit": "iter/sec",
            "range": "stddev: 0.003992018021553093",
            "extra": "mean: 3.0174878575950923 msec\nrounds: 316"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 230.80956918061048,
            "unit": "iter/sec",
            "range": "stddev: 0.00014176738346998835",
            "extra": "mean: 4.33257599999024 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 99295.39905500092,
            "unit": "iter/sec",
            "range": "stddev: 0.000003108689975537044",
            "extra": "mean: 10.070960079893409 usec\nrounds: 20015"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 150441.27019116265,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010839884563694247",
            "extra": "mean: 6.647112183573832 usec\nrounds: 37189"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11865696.874839298,
            "unit": "iter/sec",
            "range": "stddev: 9.494947838824112e-9",
            "extra": "mean: 84.2765503406932 nsec\nrounds: 66366"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3450.985451840831,
            "unit": "iter/sec",
            "range": "stddev: 0.00006556190512847695",
            "extra": "mean: 289.7723024206254 usec\nrounds: 1240"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 0.13334556390935629,
            "unit": "iter/sec",
            "range": "stddev: 14.510963292135237",
            "extra": "mean: 7.499312093199933 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 5.711008308034846,
            "unit": "iter/sec",
            "range": "stddev: 0.027404449189714537",
            "extra": "mean: 175.10042816661553 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 6.9208468977751,
            "unit": "iter/sec",
            "range": "stddev: 0.017495824836327636",
            "extra": "mean: 144.49098712492514 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.24152990557186554,
            "unit": "iter/sec",
            "range": "stddev: 0.5179563860965987",
            "extra": "mean: 4.140274048599986 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 1.4473553032905535,
            "unit": "iter/sec",
            "range": "stddev: 0.04563815162932675",
            "extra": "mean: 690.9153528000388 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 0.028278266886477697,
            "unit": "iter/sec",
            "range": "stddev: 78.11881073880318",
            "extra": "mean: 35.3628461041998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 145.8670557304668,
            "unit": "iter/sec",
            "range": "stddev: 0.0002572978573807826",
            "extra": "mean: 6.855557582843109 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 149837.48315758948,
            "unit": "iter/sec",
            "range": "stddev: 0.00000386634774830501",
            "extra": "mean: 6.6738974716244 usec\nrounds: 10046"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16411.00550705558,
            "unit": "iter/sec",
            "range": "stddev: 0.000005902214717555815",
            "extra": "mean: 60.93471844671981 usec\nrounds: 8350"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.1209270258663384,
            "unit": "iter/sec",
            "range": "stddev: 0.19032009477007464",
            "extra": "mean: 8.269450049199985 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.13621609515459498,
            "unit": "iter/sec",
            "range": "stddev: 0.45930640465750444",
            "extra": "mean: 7.341276365800058 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.25154471844494697,
            "unit": "iter/sec",
            "range": "stddev: 0.3149007190794823",
            "extra": "mean: 3.9754362810001114 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.30741589853693546,
            "unit": "iter/sec",
            "range": "stddev: 0.43297470754266104",
            "extra": "mean: 3.252922196799955 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.3320022646084284,
            "unit": "iter/sec",
            "range": "stddev: 0.49340360667935684",
            "extra": "mean: 3.0120276474000094 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.1730342162897016,
            "unit": "iter/sec",
            "range": "stddev: 0.4046133256717428",
            "extra": "mean: 5.779203798199978 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.19326627715739067,
            "unit": "iter/sec",
            "range": "stddev: 0.6256998504686329",
            "extra": "mean: 5.174208427400027 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.2291873602932837,
            "unit": "iter/sec",
            "range": "stddev: 0.4987563328007374",
            "extra": "mean: 4.363242365199949 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.23449272238141877,
            "unit": "iter/sec",
            "range": "stddev: 0.33732925789483026",
            "extra": "mean: 4.26452467199997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.49133518081043226,
            "unit": "iter/sec",
            "range": "stddev: 0.4429299643582772",
            "extra": "mean: 2.035270501799914 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.8848916174606006,
            "unit": "iter/sec",
            "range": "stddev: 0.15854670685988337",
            "extra": "mean: 1.1300818996000088 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 6.000625151983256,
            "unit": "iter/sec",
            "range": "stddev: 0.011133068115587123",
            "extra": "mean: 166.64930314293866 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.15350854876744513,
            "unit": "iter/sec",
            "range": "stddev: 1.0342786360428722",
            "extra": "mean: 6.514295184399998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.13732488965542122,
            "unit": "iter/sec",
            "range": "stddev: 1.297887827362406",
            "extra": "mean: 7.282001117999971 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.08951129332641157,
            "unit": "iter/sec",
            "range": "stddev: 1.310628260632312",
            "extra": "mean: 11.17177467599986 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.08315809530609743,
            "unit": "iter/sec",
            "range": "stddev: 1.6072110054900648",
            "extra": "mean: 12.025287451799977 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.0802962693157644,
            "unit": "iter/sec",
            "range": "stddev: 1.847199348690756",
            "extra": "mean: 12.453878723400067 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.059611047547658336,
            "unit": "iter/sec",
            "range": "stddev: 0.20364375754778574",
            "extra": "mean: 16.77541397340001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.1877252363076509,
            "unit": "iter/sec",
            "range": "stddev: 0.11715829652155098",
            "extra": "mean: 5.326934298599918 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.1850083548300393,
            "unit": "iter/sec",
            "range": "stddev: 0.12174668199389148",
            "extra": "mean: 5.4051613015999465 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.18442947936877954,
            "unit": "iter/sec",
            "range": "stddev: 0.09892608807897695",
            "extra": "mean: 5.422126676399875 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.17888188045792558,
            "unit": "iter/sec",
            "range": "stddev: 0.06998472124131062",
            "extra": "mean: 5.590281125399997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.16838672512520064,
            "unit": "iter/sec",
            "range": "stddev: 0.1408877342178761",
            "extra": "mean: 5.938710425400041 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.08120343354561413,
            "unit": "iter/sec",
            "range": "stddev: 0.46937544210826204",
            "extra": "mean: 12.314750206200006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.18739550820137804,
            "unit": "iter/sec",
            "range": "stddev: 0.33055177584956963",
            "extra": "mean: 5.336307201800082 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.20162050767657763,
            "unit": "iter/sec",
            "range": "stddev: 0.18668243577772486",
            "extra": "mean: 4.959812925400001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.3509383725738059,
            "unit": "iter/sec",
            "range": "stddev: 0.06234063786175482",
            "extra": "mean: 2.849503155399998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.4253595400939799,
            "unit": "iter/sec",
            "range": "stddev: 0.10260450773736302",
            "extra": "mean: 2.350952325599792 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.4458998541963567,
            "unit": "iter/sec",
            "range": "stddev: 0.08750860946119064",
            "extra": "mean: 2.2426560371998674 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.2564340060128573,
            "unit": "iter/sec",
            "range": "stddev: 0.0843467326764715",
            "extra": "mean: 3.8996388019998447 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.2919384772412411,
            "unit": "iter/sec",
            "range": "stddev: 0.06036394435388548",
            "extra": "mean: 3.4253792423999583 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.3236857228161733,
            "unit": "iter/sec",
            "range": "stddev: 0.15208681266014892",
            "extra": "mean: 3.0894164601999363 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.332111636258071,
            "unit": "iter/sec",
            "range": "stddev: 0.20731526413866316",
            "extra": "mean: 3.011035720600103 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.49934094724757294,
            "unit": "iter/sec",
            "range": "stddev: 0.07996245548022358",
            "extra": "mean: 2.002639690400156 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 1.0685212365755594,
            "unit": "iter/sec",
            "range": "stddev: 0.07074425881634745",
            "extra": "mean: 935.8728359998167 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 7.225637705468894,
            "unit": "iter/sec",
            "range": "stddev: 0.006255227482539604",
            "extra": "mean: 138.39608914284847 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.652479166371926,
            "unit": "iter/sec",
            "range": "stddev: 0.2289906797140419",
            "extra": "mean: 1.5326159845998517 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 6.739348096894622,
            "unit": "iter/sec",
            "range": "stddev: 0.01394127005970616",
            "extra": "mean: 148.38230428560044 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.4619371910081562,
            "unit": "iter/sec",
            "range": "stddev: 0.0872554338901978",
            "extra": "mean: 684.0239143997678 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 136750.71275363775,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012012397291663774",
            "extra": "mean: 7.312576145775143 usec\nrounds: 17617"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 184116.69347745125,
            "unit": "iter/sec",
            "range": "stddev: 8.163504549242658e-7",
            "extra": "mean: 5.431338034117313 usec\nrounds: 68555"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 765317.3196936867,
            "unit": "iter/sec",
            "range": "stddev: 3.7694235403661485e-7",
            "extra": "mean: 1.306647549019593 usec\nrounds: 74433"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 691667.332828766,
            "unit": "iter/sec",
            "range": "stddev: 3.712000941954136e-7",
            "extra": "mean: 1.4457817400602422 usec\nrounds: 64272"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 342.19710074537784,
            "unit": "iter/sec",
            "range": "stddev: 0.0005427783907318164",
            "extra": "mean: 2.922292438544301 msec\nrounds: 358"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 221.11731165787992,
            "unit": "iter/sec",
            "range": "stddev: 0.0008713461989167573",
            "extra": "mean: 4.522486242720033 msec\nrounds: 206"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 97543.36879552736,
            "unit": "iter/sec",
            "range": "stddev: 0.000004217892236795101",
            "extra": "mean: 10.25185014981616 usec\nrounds: 18165"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 147272.5121573143,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014732643352961516",
            "extra": "mean: 6.790133374867776 usec\nrounds: 33882"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11135961.681999996,
            "unit": "iter/sec",
            "range": "stddev: 1.0104673671338655e-8",
            "extra": "mean: 89.79915956575175 nsec\nrounds: 63658"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3606.3645427627084,
            "unit": "iter/sec",
            "range": "stddev: 0.00004842146791544896",
            "extra": "mean: 277.2875531972526 usec\nrounds: 1269"
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
          "id": "649eb965fa4efbece5f1cb9247d60796bfeec60d",
          "message": "Update acknowledgements page and add NSF logo",
          "timestamp": "2025-05-23T15:19:51-07:00",
          "tree_id": "ad3e3ca63033fc9354f63a83600a3f461f4d5163",
          "url": "https://github.com/iausathub/satchecker/commit/649eb965fa4efbece5f1cb9247d60796bfeec60d"
        },
        "date": 1748046754357,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 129338.56291531412,
            "unit": "iter/sec",
            "range": "stddev: 0.000001357870618211005",
            "extra": "mean: 7.731646134453816 usec\nrounds: 11137"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 169885.0806300103,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014790456537342866",
            "extra": "mean: 5.886332079848037 usec\nrounds: 61958"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 731245.0317333849,
            "unit": "iter/sec",
            "range": "stddev: 4.337571576467364e-7",
            "extra": "mean: 1.3675306588128784 usec\nrounds: 47735"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 676879.1582700672,
            "unit": "iter/sec",
            "range": "stddev: 4.343425916743295e-7",
            "extra": "mean: 1.477368578692463 usec\nrounds: 55733"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 317.26184292916435,
            "unit": "iter/sec",
            "range": "stddev: 0.004616813744823679",
            "extra": "mean: 3.1519705955413992 msec\nrounds: 314"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 220.1940587859807,
            "unit": "iter/sec",
            "range": "stddev: 0.00036311706248233917",
            "extra": "mean: 4.541448599991327 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 88373.28100586856,
            "unit": "iter/sec",
            "range": "stddev: 0.0000052371571421480836",
            "extra": "mean: 11.315637358010884 usec\nrounds: 11521"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 146779.20015734396,
            "unit": "iter/sec",
            "range": "stddev: 0.000001247700350043334",
            "extra": "mean: 6.812954416756753 usec\nrounds: 22245"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11141919.392189927,
            "unit": "iter/sec",
            "range": "stddev: 1.0674379195134933e-8",
            "extra": "mean: 89.75114294052044 nsec\nrounds: 112158"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3400.443186609158,
            "unit": "iter/sec",
            "range": "stddev: 0.000052428613859061374",
            "extra": "mean: 294.079314113516 usec\nrounds: 1162"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.20014474370995114,
            "unit": "iter/sec",
            "range": "stddev: 6.232841262148128",
            "extra": "mean: 4.996384024199983 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 1.6117713406651941,
            "unit": "iter/sec",
            "range": "stddev: 0.2179045986990503",
            "extra": "mean: 620.4354021999734 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.4175274180365554,
            "unit": "iter/sec",
            "range": "stddev: 0.05610333567072752",
            "extra": "mean: 413.6457740000196 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 150.2457590619318,
            "unit": "iter/sec",
            "range": "stddev: 0.00038654592270842233",
            "extra": "mean: 6.655761907980355 msec\nrounds: 163"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 160708.9342358792,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018054569101322524",
            "extra": "mean: 6.222429417223677 usec\nrounds: 10966"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16283.036197648944,
            "unit": "iter/sec",
            "range": "stddev: 0.000005858976834270554",
            "extra": "mean: 61.41360787150906 usec\nrounds: 8765"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.031141897135393396,
            "unit": "iter/sec",
            "range": "stddev: 0.19688015250506488",
            "extra": "mean: 32.111081597000066 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.032759237038004166,
            "unit": "iter/sec",
            "range": "stddev: 5.642145401238079",
            "extra": "mean: 30.525741452399963 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.02129089674054317,
            "unit": "iter/sec",
            "range": "stddev: 0.31302362841973086",
            "extra": "mean: 46.968430319599975 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.014261904311679948,
            "unit": "iter/sec",
            "range": "stddev: 57.036043273551705",
            "extra": "mean: 70.11686364919997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.03840837913757866,
            "unit": "iter/sec",
            "range": "stddev: 0.1502445452573179",
            "extra": "mean: 26.035985440000058 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.08638918544100471,
            "unit": "iter/sec",
            "range": "stddev: 0.0846565866006561",
            "extra": "mean: 11.575522965000072 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 2.865177225030991,
            "unit": "iter/sec",
            "range": "stddev: 0.015149616216102795",
            "extra": "mean: 349.01854979989366 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.02402364419500146,
            "unit": "iter/sec",
            "range": "stddev: 32.19784822102597",
            "extra": "mean: 41.62565811760014 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.02666527350439659,
            "unit": "iter/sec",
            "range": "stddev: 54.963580581810355",
            "extra": "mean: 37.50195923679985 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.017858737124400968,
            "unit": "iter/sec",
            "range": "stddev: 31.549466560361488",
            "extra": "mean: 55.99500082419981 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 131353.1646785425,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010809032072386289",
            "extra": "mean: 7.613063624673805 usec\nrounds: 15042"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 178344.75811467646,
            "unit": "iter/sec",
            "range": "stddev: 8.373775107331932e-7",
            "extra": "mean: 5.6071174200533305 usec\nrounds: 66989"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 732218.9279337716,
            "unit": "iter/sec",
            "range": "stddev: 4.5901534982712265e-7",
            "extra": "mean: 1.3657117589432883 usec\nrounds: 76717"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 684883.3205058246,
            "unit": "iter/sec",
            "range": "stddev: 4.33246777940191e-7",
            "extra": "mean: 1.4601027212364348 usec\nrounds: 58303"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 363.37516493276223,
            "unit": "iter/sec",
            "range": "stddev: 0.00019637630843125707",
            "extra": "mean: 2.7519767350777444 msec\nrounds: 385"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 229.53557236442379,
            "unit": "iter/sec",
            "range": "stddev: 0.0002334321108068942",
            "extra": "mean: 4.356623200923049 msec\nrounds: 209"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 98589.06301618971,
            "unit": "iter/sec",
            "range": "stddev: 0.000003050862421255627",
            "extra": "mean: 10.14311293166247 usec\nrounds: 19808"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 148218.57520376678,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011514062232310377",
            "extra": "mean: 6.746792691976885 usec\nrounds: 33882"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11034230.762616655,
            "unit": "iter/sec",
            "range": "stddev: 9.127291551005996e-9",
            "extra": "mean: 90.62706966288268 nsec\nrounds: 109087"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3636.7981403124854,
            "unit": "iter/sec",
            "range": "stddev: 0.00005387694172872317",
            "extra": "mean: 274.9671445647178 usec\nrounds: 1252"
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
          "id": "649eb965fa4efbece5f1cb9247d60796bfeec60d",
          "message": "Update acknowledgements page and add NSF logo",
          "timestamp": "2025-05-23T15:19:51-07:00",
          "tree_id": "ad3e3ca63033fc9354f63a83600a3f461f4d5163",
          "url": "https://github.com/iausathub/satchecker/commit/649eb965fa4efbece5f1cb9247d60796bfeec60d"
        },
        "date": 1749063034777,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 138093.7224883405,
            "unit": "iter/sec",
            "range": "stddev: 9.673083446459546e-7",
            "extra": "mean: 7.2414587859664055 usec\nrounds: 11513"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 186346.64907469467,
            "unit": "iter/sec",
            "range": "stddev: 8.279745687647588e-7",
            "extra": "mean: 5.366342807694722 usec\nrounds: 36414"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 765073.7753681244,
            "unit": "iter/sec",
            "range": "stddev: 3.8701278904243463e-7",
            "extra": "mean: 1.3070634913853088 usec\nrounds: 31768"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 683153.3574553062,
            "unit": "iter/sec",
            "range": "stddev: 7.285289742307272e-7",
            "extra": "mean: 1.463800168859483 usec\nrounds: 28429"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 310.3405622736191,
            "unit": "iter/sec",
            "range": "stddev: 0.005660959996015748",
            "extra": "mean: 3.222266508360342 msec\nrounds: 299"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 191.5452097646241,
            "unit": "iter/sec",
            "range": "stddev: 0.0010763362977414582",
            "extra": "mean: 5.220699599999534 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 77838.69689404772,
            "unit": "iter/sec",
            "range": "stddev: 0.000054347930135908216",
            "extra": "mean: 12.847080435598471 usec\nrounds: 12395"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152369.08917490882,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011927026104195979",
            "extra": "mean: 6.563010945429171 usec\nrounds: 26130"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11535128.883671964,
            "unit": "iter/sec",
            "range": "stddev: 1.6791503346454064e-8",
            "extra": "mean: 86.69170583914504 nsec\nrounds: 119689"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3428.5478056879265,
            "unit": "iter/sec",
            "range": "stddev: 0.00005902300404012381",
            "extra": "mean: 291.66867626608854 usec\nrounds: 1146"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 0.3467714521813505,
            "unit": "iter/sec",
            "range": "stddev: 5.800235238184709",
            "extra": "mean: 2.8837437271999873 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 3.862132047930915,
            "unit": "iter/sec",
            "range": "stddev: 0.03620418499531588",
            "extra": "mean: 258.92434219998677 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 3.908240234699859,
            "unit": "iter/sec",
            "range": "stddev: 0.054807522001061426",
            "extra": "mean: 255.8696343999941 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.6963316102659598,
            "unit": "iter/sec",
            "range": "stddev: 0.06341389275074645",
            "extra": "mean: 1.4360973784000066 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.0686204094411176,
            "unit": "iter/sec",
            "range": "stddev: 0.12873711323982323",
            "extra": "mean: 483.41396780000423 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 2.8684981693967964,
            "unit": "iter/sec",
            "range": "stddev: 0.0653645600941537",
            "extra": "mean: 348.6144807999949 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 3.915976085328535,
            "unit": "iter/sec",
            "range": "stddev: 0.023180543012901747",
            "extra": "mean: 255.3641743999833 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 4.345264217414501,
            "unit": "iter/sec",
            "range": "stddev: 0.007816440179054982",
            "extra": "mean: 230.13560280001002 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 4.5263978631674995,
            "unit": "iter/sec",
            "range": "stddev: 0.00792740318730839",
            "extra": "mean: 220.92622660002235 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.7096483023293318,
            "unit": "iter/sec",
            "range": "stddev: 0.03648429856737388",
            "extra": "mean: 1.409148724399995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.341835673746764,
            "unit": "iter/sec",
            "range": "stddev: 0.1045769618149804",
            "extra": "mean: 427.0154439999942 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.0483351817971145,
            "unit": "iter/sec",
            "range": "stddev: 0.053421092626341996",
            "extra": "mean: 328.04791479999267 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 3.96109649323913,
            "unit": "iter/sec",
            "range": "stddev: 0.013123735374945416",
            "extra": "mean: 252.45534959999532 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 4.099341920589119,
            "unit": "iter/sec",
            "range": "stddev: 0.029978150423236642",
            "extra": "mean: 243.94159340001806 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 4.41749778257719,
            "unit": "iter/sec",
            "range": "stddev: 0.01486930446396019",
            "extra": "mean: 226.3724962000083 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.6979277608958118,
            "unit": "iter/sec",
            "range": "stddev: 0.04089741046614777",
            "extra": "mean: 1.432813044600016 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.2907106885746553,
            "unit": "iter/sec",
            "range": "stddev: 0.09873658600350615",
            "extra": "mean: 436.5457431999971 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.9123954828778964,
            "unit": "iter/sec",
            "range": "stddev: 0.07495471258898963",
            "extra": "mean: 343.35996119999663 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 132.40376609950317,
            "unit": "iter/sec",
            "range": "stddev: 0.0012168173585039728",
            "extra": "mean: 7.55265525641081 msec\nrounds: 156"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 149847.56300085192,
            "unit": "iter/sec",
            "range": "stddev: 0.0000037702262607724973",
            "extra": "mean: 6.673448536459112 usec\nrounds: 9123"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16277.136277739028,
            "unit": "iter/sec",
            "range": "stddev: 0.000006716689398783901",
            "extra": "mean: 61.43586825943223 usec\nrounds: 7826"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.13814100104177005,
            "unit": "iter/sec",
            "range": "stddev: 0.16691926438680524",
            "extra": "mean: 7.238980407400026 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.15609018903547167,
            "unit": "iter/sec",
            "range": "stddev: 0.12738451503387288",
            "extra": "mean: 6.406552559000033 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.2771756561189307,
            "unit": "iter/sec",
            "range": "stddev: 0.09518521035758885",
            "extra": "mean: 3.6078204486000005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.3337224717786918,
            "unit": "iter/sec",
            "range": "stddev: 0.05031435409789107",
            "extra": "mean: 2.996501837799974 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.37675156168519697,
            "unit": "iter/sec",
            "range": "stddev: 0.0427948444693601",
            "extra": "mean: 2.6542690242000164 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.1938162341299502,
            "unit": "iter/sec",
            "range": "stddev: 0.08745344970986699",
            "extra": "mean: 5.159526519999963 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.21074467864422847,
            "unit": "iter/sec",
            "range": "stddev: 0.16532406620703222",
            "extra": "mean: 4.745078293000051 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.24057496410239737,
            "unit": "iter/sec",
            "range": "stddev: 0.14475431235370503",
            "extra": "mean: 4.156708507600001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.2524654777021851,
            "unit": "iter/sec",
            "range": "stddev: 0.14150108644382006",
            "extra": "mean: 3.9609375867999916 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.39712230692556444,
            "unit": "iter/sec",
            "range": "stddev: 0.06891040011543047",
            "extra": "mean: 2.5181159118000322 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.8252366421651012,
            "unit": "iter/sec",
            "range": "stddev: 0.054888188307220614",
            "extra": "mean: 1.2117736282000124 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 4.160173367536766,
            "unit": "iter/sec",
            "range": "stddev: 0.006435252121505081",
            "extra": "mean: 240.37459780001882 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.13633996689387895,
            "unit": "iter/sec",
            "range": "stddev: 0.19402185621290463",
            "extra": "mean: 7.334606445799977 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.11902340249513678,
            "unit": "iter/sec",
            "range": "stddev: 0.2781201670954259",
            "extra": "mean: 8.401709067600041 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.06957229587173082,
            "unit": "iter/sec",
            "range": "stddev: 0.15732056243639314",
            "extra": "mean: 14.373537447199988 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.053227897447407586,
            "unit": "iter/sec",
            "range": "stddev: 6.517192963681396",
            "extra": "mean: 18.787140728000033 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.05389083846160914,
            "unit": "iter/sec",
            "range": "stddev: 0.32505846597405313",
            "extra": "mean: 18.556029717599994 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.03760796544729806,
            "unit": "iter/sec",
            "range": "stddev: 0.29255512492900804",
            "extra": "mean: 26.590111645399976 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.136807678061432,
            "unit": "iter/sec",
            "range": "stddev: 0.24143467483936767",
            "extra": "mean: 7.309531264399948 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.13661817642465166,
            "unit": "iter/sec",
            "range": "stddev: 0.16525130511546385",
            "extra": "mean: 7.3196702383999765 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.1343342079853222,
            "unit": "iter/sec",
            "range": "stddev: 0.173391665980295",
            "extra": "mean: 7.444120265400033 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.13209382660686966,
            "unit": "iter/sec",
            "range": "stddev: 0.15600985913238066",
            "extra": "mean: 7.570376494400034 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.12023492865363392,
            "unit": "iter/sec",
            "range": "stddev: 0.21974634846227145",
            "extra": "mean: 8.317050720600037 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.06341567116190021,
            "unit": "iter/sec",
            "range": "stddev: 0.5926530695848109",
            "extra": "mean: 15.768972900200016 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.13920938821948836,
            "unit": "iter/sec",
            "range": "stddev: 0.26607483499007173",
            "extra": "mean: 7.183423566400006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.15817411813029333,
            "unit": "iter/sec",
            "range": "stddev: 0.18835180466806575",
            "extra": "mean: 6.322146832999988 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.26417975367578067,
            "unit": "iter/sec",
            "range": "stddev: 0.16755253886707963",
            "extra": "mean: 3.785301432399956 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.32430663928375764,
            "unit": "iter/sec",
            "range": "stddev: 0.057768835236201715",
            "extra": "mean: 3.083501473199976 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.3558306918677234,
            "unit": "iter/sec",
            "range": "stddev: 0.06101899650814119",
            "extra": "mean: 2.8103253115999904 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.1944882937783995,
            "unit": "iter/sec",
            "range": "stddev: 0.050197402025268054",
            "extra": "mean: 5.141697634200045 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.2137760439692925,
            "unit": "iter/sec",
            "range": "stddev: 0.050931361284711284",
            "extra": "mean: 4.677792616199985 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.2372040990729496,
            "unit": "iter/sec",
            "range": "stddev: 0.14852138917196858",
            "extra": "mean: 4.215778748800039 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.24898767327558596,
            "unit": "iter/sec",
            "range": "stddev: 0.10597478750273948",
            "extra": "mean: 4.016263081799934 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.376457188952941,
            "unit": "iter/sec",
            "range": "stddev: 0.06782721006781936",
            "extra": "mean: 2.656344544199965 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.873555753919084,
            "unit": "iter/sec",
            "range": "stddev: 0.009697441713808586",
            "extra": "mean: 1.1447466238000743 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 4.525727434426992,
            "unit": "iter/sec",
            "range": "stddev: 0.0182960131467724",
            "extra": "mean: 220.9589539999797 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.5941994901294905,
            "unit": "iter/sec",
            "range": "stddev: 0.06426796923174939",
            "extra": "mean: 1.6829364827998687 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 3.1788061214161702,
            "unit": "iter/sec",
            "range": "stddev: 0.010444194224831782",
            "extra": "mean: 314.58351400005995 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.3464339746939944,
            "unit": "iter/sec",
            "range": "stddev: 0.06365981162095048",
            "extra": "mean: 742.7025898000466 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 138081.11276362097,
            "unit": "iter/sec",
            "range": "stddev: 0.000002738021206954484",
            "extra": "mean: 7.242120084242696 usec\nrounds: 17213"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 189307.72844753854,
            "unit": "iter/sec",
            "range": "stddev: 9.300643116958434e-7",
            "extra": "mean: 5.282404517769715 usec\nrounds: 39175"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 781997.2070047597,
            "unit": "iter/sec",
            "range": "stddev: 3.7498035881348384e-7",
            "extra": "mean: 1.2787769458029705 usec\nrounds: 37722"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 716899.6518551541,
            "unit": "iter/sec",
            "range": "stddev: 3.7304398714892324e-7",
            "extra": "mean: 1.3948953628478604 usec\nrounds: 36536"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 350.3548683906785,
            "unit": "iter/sec",
            "range": "stddev: 0.00015773700038335212",
            "extra": "mean: 2.8542489065255583 msec\nrounds: 353"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 220.36223546466832,
            "unit": "iter/sec",
            "range": "stddev: 0.00023678873797307345",
            "extra": "mean: 4.537982644309916 msec\nrounds: 194"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 79981.6544346798,
            "unit": "iter/sec",
            "range": "stddev: 0.000005242872535223127",
            "extra": "mean: 12.502867152075353 usec\nrounds: 7806"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 144723.7193384634,
            "unit": "iter/sec",
            "range": "stddev: 0.0000022375072592703085",
            "extra": "mean: 6.909717388214116 usec\nrounds: 27773"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 9990311.01969926,
            "unit": "iter/sec",
            "range": "stddev: 1.928373837904849e-8",
            "extra": "mean: 100.09698377037095 nsec\nrounds: 194553"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3548.2729021900427,
            "unit": "iter/sec",
            "range": "stddev: 0.00005011908291342047",
            "extra": "mean: 281.8272516138165 usec\nrounds: 1236"
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
          "id": "c77820f640f33fb9cb694c3f60fcafdddfa6d5a8",
          "message": "Add additional constellations to supplemental TLE collection",
          "timestamp": "2025-06-13T10:32:58-07:00",
          "tree_id": "9512329e12bc79604212986fede41abce53d4d9d",
          "url": "https://github.com/iausathub/satchecker/commit/c77820f640f33fb9cb694c3f60fcafdddfa6d5a8"
        },
        "date": 1749836098126,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 135867.91306743908,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011370380302646717",
            "extra": "mean: 7.360089497390324 usec\nrounds: 12235"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 183988.23506313446,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011596385816908875",
            "extra": "mean: 5.435130130232816 usec\nrounds: 51825"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 751346.7320592307,
            "unit": "iter/sec",
            "range": "stddev: 4.441028705563042e-7",
            "extra": "mean: 1.3309434344104758 usec\nrounds: 64898"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 686363.4510194074,
            "unit": "iter/sec",
            "range": "stddev: 4.4937536050641656e-7",
            "extra": "mean: 1.4569540358169863 usec\nrounds: 70294"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 303.7750392668944,
            "unit": "iter/sec",
            "range": "stddev: 0.0043703277796368015",
            "extra": "mean: 3.291909705331016 msec\nrounds: 319"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 229.15829379562996,
            "unit": "iter/sec",
            "range": "stddev: 0.00018332873233758932",
            "extra": "mean: 4.363795799997661 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 104950.37325451915,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029947277913625695",
            "extra": "mean: 9.528312944393843 usec\nrounds: 25161"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 150964.6455021858,
            "unit": "iter/sec",
            "range": "stddev: 0.000001312608580730817",
            "extra": "mean: 6.624067487281459 usec\nrounds: 30302"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12399671.658226186,
            "unit": "iter/sec",
            "range": "stddev: 1.0064166425681268e-8",
            "extra": "mean: 80.64729676426163 nsec\nrounds: 126663"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3586.2159848078245,
            "unit": "iter/sec",
            "range": "stddev: 0.00004901568299733381",
            "extra": "mean: 278.8454471889783 usec\nrounds: 1174"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 150.3280819819068,
            "unit": "iter/sec",
            "range": "stddev: 0.00007835833387501373",
            "extra": "mean: 6.652117068322325 msec\nrounds: 161"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 157958.34380463863,
            "unit": "iter/sec",
            "range": "stddev: 0.000003020518755305406",
            "extra": "mean: 6.330783014772492 usec\nrounds: 10715"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 16035.223338785217,
            "unit": "iter/sec",
            "range": "stddev: 0.000008260583968458294",
            "extra": "mean: 62.36271106877874 usec\nrounds: 7725"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 135924.83169966913,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017724619822745601",
            "extra": "mean: 7.3570074540135275 usec\nrounds: 17171"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 185825.89729783547,
            "unit": "iter/sec",
            "range": "stddev: 7.899035989356372e-7",
            "extra": "mean: 5.381381252782187 usec\nrounds: 47239"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 755128.4839014227,
            "unit": "iter/sec",
            "range": "stddev: 3.644273803801515e-7",
            "extra": "mean: 1.3242779491424188 usec\nrounds: 74600"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 688539.7804487986,
            "unit": "iter/sec",
            "range": "stddev: 4.175075293501492e-7",
            "extra": "mean: 1.452348910542522 usec\nrounds: 84589"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 356.6297300513213,
            "unit": "iter/sec",
            "range": "stddev: 0.00025807630494575857",
            "extra": "mean: 2.804028704662658 msec\nrounds: 386"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 190.69517216322242,
            "unit": "iter/sec",
            "range": "stddev: 0.007010885449024211",
            "extra": "mean: 5.243971248228908 msec\nrounds: 141"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 104174.29094607447,
            "unit": "iter/sec",
            "range": "stddev: 0.000014241707974677269",
            "extra": "mean: 9.599297397835395 usec\nrounds: 28551"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153304.8815954655,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010392372190595263",
            "extra": "mean: 6.522949495103217 usec\nrounds: 39719"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11710646.487204554,
            "unit": "iter/sec",
            "range": "stddev: 8.643426539174293e-9",
            "extra": "mean: 85.39238214495894 nsec\nrounds: 114208"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3539.2864085620995,
            "unit": "iter/sec",
            "range": "stddev: 0.000050695427541801484",
            "extra": "mean: 282.542830549356 usec\nrounds: 1257"
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
          "id": "b76c7409a490067561f989d9ceb4314451ef7eab",
          "message": "Temporarily disable tests related to caching and fix formatting error",
          "timestamp": "2025-06-13T10:54:31-07:00",
          "tree_id": "475b2421e6ae20a62d44491da730611caf547cd1",
          "url": "https://github.com/iausathub/satchecker/commit/b76c7409a490067561f989d9ceb4314451ef7eab"
        },
        "date": 1749837391703,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec",
            "value": 134541.9617212314,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011457180525227779",
            "extra": "mean: 7.432625384725567 usec\nrounds: 11692"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 183348.30233106558,
            "unit": "iter/sec",
            "range": "stddev: 8.160650591719096e-7",
            "extra": "mean: 5.454100132295391 usec\nrounds: 43912"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_jd_to_gst",
            "value": 758793.29608673,
            "unit": "iter/sec",
            "range": "stddev: 3.741540105332139e-7",
            "extra": "mean: 1.3178819649003595 usec\nrounds: 57627"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_calculate_lst",
            "value": 695672.7790936902,
            "unit": "iter/sec",
            "range": "stddev: 4.37704976722923e-7",
            "extra": "mean: 1.43745742258707 usec\nrounds: 61993"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 332.71771289486577,
            "unit": "iter/sec",
            "range": "stddev: 0.004071395253632182",
            "extra": "mean: 3.00555083556969 msec\nrounds: 298"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 214.6089091711889,
            "unit": "iter/sec",
            "range": "stddev: 0.0007250884962193422",
            "extra": "mean: 4.659638800001176 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_is_illuminated",
            "value": 100398.23598556517,
            "unit": "iter/sec",
            "range": "stddev: 0.000003987873592127858",
            "extra": "mean: 9.960334364278827 usec\nrounds: 18106"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_phase_angle",
            "value": 153181.8231752901,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011056736781345216",
            "extra": "mean: 6.528189698171127 usec\nrounds: 27781"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12559183.24324051,
            "unit": "iter/sec",
            "range": "stddev: 9.851317831183406e-9",
            "extra": "mean: 79.62301215236235 nsec\nrounds: 70687"
          },
          {
            "name": "tests/benchmark/test_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3601.4948371718197,
            "unit": "iter/sec",
            "range": "stddev: 0.00004846362282283641",
            "extra": "mean: 277.6624832774381 usec\nrounds: 1196"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 148.2265392675508,
            "unit": "iter/sec",
            "range": "stddev: 0.00027941374603669624",
            "extra": "mean: 6.746430193549801 msec\nrounds: 155"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 156892.96596522917,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032738477893104794",
            "extra": "mean: 6.373772041645393 usec\nrounds: 10673"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 15695.951649082728,
            "unit": "iter/sec",
            "range": "stddev: 0.000008617629724244523",
            "extra": "mean: 63.71069574863528 usec\nrounds: 8562"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 133907.28674107793,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013951064074434635",
            "extra": "mean: 7.467853500262403 usec\nrounds: 16628"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 184273.82878466253,
            "unit": "iter/sec",
            "range": "stddev: 9.067462869460333e-7",
            "extra": "mean: 5.426706584409082 usec\nrounds: 64608"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 744039.4334940478,
            "unit": "iter/sec",
            "range": "stddev: 3.96818142322925e-7",
            "extra": "mean: 1.3440147860227623 usec\nrounds: 71757"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 703117.0934665487,
            "unit": "iter/sec",
            "range": "stddev: 4.151735384861426e-7",
            "extra": "mean: 1.4222382150741664 usec\nrounds: 77556"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 358.8359873888447,
            "unit": "iter/sec",
            "range": "stddev: 0.0002209180970981758",
            "extra": "mean: 2.7867884915243244 msec\nrounds: 354"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 210.92579212939683,
            "unit": "iter/sec",
            "range": "stddev: 0.0055956094516851984",
            "extra": "mean: 4.741003885321569 msec\nrounds: 218"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 106483.88055836903,
            "unit": "iter/sec",
            "range": "stddev: 0.000003416998223448343",
            "extra": "mean: 9.391092762174939 usec\nrounds: 27619"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 152586.45988085485,
            "unit": "iter/sec",
            "range": "stddev: 0.000001051269758703205",
            "extra": "mean: 6.553661450569316 usec\nrounds: 39876"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11129838.894968448,
            "unit": "iter/sec",
            "range": "stddev: 1.5100405959188338e-8",
            "extra": "mean: 89.84856020261053 nsec\nrounds: 195313"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 3522.607541520846,
            "unit": "iter/sec",
            "range": "stddev: 0.00004740298511983279",
            "extra": "mean: 283.8806163369142 usec\nrounds: 1212"
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
          "id": "29f1fdf64f888ca80752aa7445208895f02074d1",
          "message": "Merge pull request #155 from iausathub/alert-autofix-17\n\nPotential fix for code scanning alert no. 17: Workflow does not contain permissions",
          "timestamp": "2025-07-01T20:55:13-07:00",
          "tree_id": "771e707b5b34a0c3f4fb1fa05e934bf482891c44",
          "url": "https://github.com/iausathub/satchecker/commit/29f1fdf64f888ca80752aa7445208895f02074d1"
        },
        "date": 1751475898070,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 704.4622895705182,
            "unit": "iter/sec",
            "range": "stddev: 0.0001227335845204648",
            "extra": "mean: 1.4195223999990958 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12588325.972111242,
            "unit": "iter/sec",
            "range": "stddev: 8.919567288960574e-9",
            "extra": "mean: 79.43868010859948 nsec\nrounds: 128950"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 143239.96651369054,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010740575490919167",
            "extra": "mean: 6.98129177448825 usec\nrounds: 20108"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 201887.92567437384,
            "unit": "iter/sec",
            "range": "stddev: 7.460416467871397e-7",
            "extra": "mean: 4.953243224723135 usec\nrounds: 78964"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1436.3986931075892,
            "unit": "iter/sec",
            "range": "stddev: 0.00002264322654569156",
            "extra": "mean: 696.1855401278187 usec\nrounds: 785"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4180.278505226983,
            "unit": "iter/sec",
            "range": "stddev: 0.00001485437822522453",
            "extra": "mean: 239.21851109910716 usec\nrounds: 1847"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 734410.3718066553,
            "unit": "iter/sec",
            "range": "stddev: 4.207621928076725e-7",
            "extra": "mean: 1.3616365432584947 usec\nrounds: 62775"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 163878.79580821205,
            "unit": "iter/sec",
            "range": "stddev: 9.002112994962161e-7",
            "extra": "mean: 6.10207071066292 usec\nrounds: 33630"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 414.1818011019817,
            "unit": "iter/sec",
            "range": "stddev: 0.0035437267815411878",
            "extra": "mean: 2.4143986948228453 msec\nrounds: 367"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 672227.858361413,
            "unit": "iter/sec",
            "range": "stddev: 4.283408854240969e-7",
            "extra": "mean: 1.4875908333188494 usec\nrounds: 74378"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133286.80750534806,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010912106879012254",
            "extra": "mean: 7.502617991355788 usec\nrounds: 29392"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 1.7989068071396033,
            "unit": "iter/sec",
            "range": "stddev: 0.12281505484383727",
            "extra": "mean: 555.8931657999977 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.5007805061306996,
            "unit": "iter/sec",
            "range": "stddev: 0.21940184888333955",
            "extra": "mean: 1.9968828413999973 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.210940991161797,
            "unit": "iter/sec",
            "range": "stddev: 0.04202770166219306",
            "extra": "mean: 825.804070800001 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.11653750420130433,
            "unit": "iter/sec",
            "range": "stddev: 7.646165756270054",
            "extra": "mean: 8.5809285762 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 95840.1897463499,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017107075739841356",
            "extra": "mean: 10.434036103711755 usec\nrounds: 13295"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.12342766024174198,
            "unit": "iter/sec",
            "range": "stddev: 8.080995799749266",
            "extra": "mean: 8.101911662600003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.380272526339932,
            "unit": "iter/sec",
            "range": "stddev: 0.12273770866355417",
            "extra": "mean: 2.629692998400003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.5464422599683856,
            "unit": "iter/sec",
            "range": "stddev: 0.11462299925479373",
            "extra": "mean: 1.8300195157999952 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.37418539830370295,
            "unit": "iter/sec",
            "range": "stddev: 0.07385336296908637",
            "extra": "mean: 2.672472000599987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.31730109873045004,
            "unit": "iter/sec",
            "range": "stddev: 0.3249978657590722",
            "extra": "mean: 3.151580640600014 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.6969051529469105,
            "unit": "iter/sec",
            "range": "stddev: 0.057630886464408476",
            "extra": "mean: 1.4349154913999882 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 3.4518709118251936,
            "unit": "iter/sec",
            "range": "stddev: 0.007354584964307092",
            "extra": "mean: 289.69797119998475 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 1.035060397774994,
            "unit": "iter/sec",
            "range": "stddev: 0.05005023042104896",
            "extra": "mean: 966.1271961999887 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 3.2374720723276895,
            "unit": "iter/sec",
            "range": "stddev: 0.018658710039483963",
            "extra": "mean: 308.8829733999887 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.10520931767981943,
            "unit": "iter/sec",
            "range": "stddev: 0.7198218461538801",
            "extra": "mean: 9.504861565999999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.39748862637830484,
            "unit": "iter/sec",
            "range": "stddev: 0.08436675310541879",
            "extra": "mean: 2.5157952545999707 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.2740243717994199,
            "unit": "iter/sec",
            "range": "stddev: 0.21128765358670282",
            "extra": "mean: 3.649310437000031 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.49398281933464716,
            "unit": "iter/sec",
            "range": "stddev: 0.06835368675976555",
            "extra": "mean: 2.0243619026000035 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.41320565878892057,
            "unit": "iter/sec",
            "range": "stddev: 0.22546645114771072",
            "extra": "mean: 2.4201023842000042 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.130670304993493,
            "unit": "iter/sec",
            "range": "stddev: 0.8193700963887034",
            "extra": "mean: 7.652848135999966 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.2793794383216,
            "unit": "iter/sec",
            "range": "stddev: 0.07042860276647384",
            "extra": "mean: 3.579361480600005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.26467318516322,
            "unit": "iter/sec",
            "range": "stddev: 0.037787610540481534",
            "extra": "mean: 3.7782444768000003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.4561209951090879,
            "unit": "iter/sec",
            "range": "stddev: 0.06458781776795065",
            "extra": "mean: 2.1924007242000245 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.47341501699031546,
            "unit": "iter/sec",
            "range": "stddev: 0.07511378127270688",
            "extra": "mean: 2.112311532400031 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.26157298941129536,
            "unit": "iter/sec",
            "range": "stddev: 0.250064441823603",
            "extra": "mean: 3.8230247024000166 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.3115363255021086,
            "unit": "iter/sec",
            "range": "stddev: 0.06583303134532105",
            "extra": "mean: 3.2098985515999856 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.2789107434796086,
            "unit": "iter/sec",
            "range": "stddev: 0.1528535556702223",
            "extra": "mean: 3.585376409399987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.6196227245467467,
            "unit": "iter/sec",
            "range": "stddev: 0.07917894485415368",
            "extra": "mean: 1.6138852891999704 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.3910673941341593,
            "unit": "iter/sec",
            "range": "stddev: 0.13225111809456688",
            "extra": "mean: 2.5571040055999674 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.3218399412506585,
            "unit": "iter/sec",
            "range": "stddev: 0.09174839134591672",
            "extra": "mean: 3.107134546799989 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.07701854446242737,
            "unit": "iter/sec",
            "range": "stddev: 0.3901837776522691",
            "extra": "mean: 12.983885984599965 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 1.4966833483529831,
            "unit": "iter/sec",
            "range": "stddev: 0.03410203356067866",
            "extra": "mean: 668.144000600023 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.3090214047988714,
            "unit": "iter/sec",
            "range": "stddev: 0.11751182224285256",
            "extra": "mean: 3.236021791600024 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18616.967703822014,
            "unit": "iter/sec",
            "range": "stddev: 0.000005410461156297301",
            "extra": "mean: 53.71444028420926 usec\nrounds: 8599"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 221.28678677490524,
            "unit": "iter/sec",
            "range": "stddev: 0.00010536019316384657",
            "extra": "mean: 4.519022642853088 msec\nrounds: 196"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.5047554480099958,
            "unit": "iter/sec",
            "range": "stddev: 0.3913637454272631",
            "extra": "mean: 1.9811574178000684 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.7807944774259086,
            "unit": "iter/sec",
            "range": "stddev: 0.048876871822235574",
            "extra": "mean: 1.2807467636000183 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.12774434483145403,
            "unit": "iter/sec",
            "range": "stddev: 0.2722240140699352",
            "extra": "mean: 7.828135181400012 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.11070543916000852,
            "unit": "iter/sec",
            "range": "stddev: 0.1760371702384032",
            "extra": "mean: 9.032979839000017 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.7500812306094289,
            "unit": "iter/sec",
            "range": "stddev: 0.023758091377691602",
            "extra": "mean: 1.3331889390000016 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.630618584486282,
            "unit": "iter/sec",
            "range": "stddev: 0.12690156269860772",
            "extra": "mean: 1.5857445761999316 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.23942265345913064,
            "unit": "iter/sec",
            "range": "stddev: 0.044962823268127006",
            "extra": "mean: 4.176714214599997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 3.385288449747474,
            "unit": "iter/sec",
            "range": "stddev: 0.02806766964713491",
            "extra": "mean: 295.3958030000649 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 3.0651545208271416,
            "unit": "iter/sec",
            "range": "stddev: 0.040364845183404316",
            "extra": "mean: 326.24782640000376 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 3.4284367282311776,
            "unit": "iter/sec",
            "range": "stddev: 0.03743963208979693",
            "extra": "mean: 291.67812599998797 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.6206520531171775,
            "unit": "iter/sec",
            "range": "stddev: 0.07516012800605373",
            "extra": "mean: 381.58442239996475 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 3.599317321226934,
            "unit": "iter/sec",
            "range": "stddev: 0.014036096938089167",
            "extra": "mean: 277.830463600003 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.9932551100728575,
            "unit": "iter/sec",
            "range": "stddev: 0.00789222480763731",
            "extra": "mean: 1.006790692399909 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 3.5717864516742166,
            "unit": "iter/sec",
            "range": "stddev: 0.01156636932727914",
            "extra": "mean: 279.9719450000339 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.605043619324665,
            "unit": "iter/sec",
            "range": "stddev: 0.06611785110682045",
            "extra": "mean: 383.8707315999727 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 3.6591840378191476,
            "unit": "iter/sec",
            "range": "stddev: 0.009523532651023254",
            "extra": "mean: 273.28497000003154 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 3.4529060376111,
            "unit": "iter/sec",
            "range": "stddev: 0.01309498942249701",
            "extra": "mean: 289.61112439997123 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.9965434108511552,
            "unit": "iter/sec",
            "range": "stddev: 0.005741090816487823",
            "extra": "mean: 1.0034685785999955 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 3.3697762458187794,
            "unit": "iter/sec",
            "range": "stddev: 0.02564083894144856",
            "extra": "mean: 296.75560840005346 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 3.451489324788592,
            "unit": "iter/sec",
            "range": "stddev: 0.017435210209038085",
            "extra": "mean: 289.72999939996953 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 2.970187107488997,
            "unit": "iter/sec",
            "range": "stddev: 0.037668257723620424",
            "extra": "mean: 336.67912620003335 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.6013642467702938,
            "unit": "iter/sec",
            "range": "stddev: 0.07154547267791167",
            "extra": "mean: 384.4136788000924 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.9812906094202098,
            "unit": "iter/sec",
            "range": "stddev: 0.02346350768412892",
            "extra": "mean: 1.0190661058000388 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.00210519144137,
            "unit": "iter/sec",
            "range": "stddev: 0.04405130490603277",
            "extra": "mean: 333.0995871999676 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 3.455258319568944,
            "unit": "iter/sec",
            "range": "stddev: 0.010957286551559508",
            "extra": "mean: 289.413962000026 msec\nrounds: 5"
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
          "id": "1eef6b1657bfc1f8ad0b084f00f32123bac6ec0a",
          "message": "Disable ephemeris data collection temporarily",
          "timestamp": "2025-07-15T13:00:46-07:00",
          "tree_id": "db46613bfaa1e983f7c03406a3d58ca65cca9e38",
          "url": "https://github.com/iausathub/satchecker/commit/1eef6b1657bfc1f8ad0b084f00f32123bac6ec0a"
        },
        "date": 1752615500449,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 144270.43517350897,
            "unit": "iter/sec",
            "range": "stddev: 8.762887873102833e-7",
            "extra": "mean: 6.931427071647321 usec\nrounds: 11717"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 112170.49907716415,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027238265474425158",
            "extra": "mean: 8.915000006481932 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1418.1244659242689,
            "unit": "iter/sec",
            "range": "stddev: 0.00001951786417360975",
            "extra": "mean: 705.1567221557282 usec\nrounds: 835"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4000.4790813035734,
            "unit": "iter/sec",
            "range": "stddev: 0.00003679811178610176",
            "extra": "mean: 249.97006100432992 usec\nrounds: 1672"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 126440.86545717494,
            "unit": "iter/sec",
            "range": "stddev: 0.0000024301425996852843",
            "extra": "mean: 7.908835457462891 usec\nrounds: 19618"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12602811.749229126,
            "unit": "iter/sec",
            "range": "stddev: 9.001058157724097e-9",
            "extra": "mean: 79.34737262594933 nsec\nrounds: 126183"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 742.8407848130422,
            "unit": "iter/sec",
            "range": "stddev: 0.00006447308182289445",
            "extra": "mean: 1.3461834897119704 msec\nrounds: 486"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 416.419498291269,
            "unit": "iter/sec",
            "range": "stddev: 0.0048253248896694195",
            "extra": "mean: 2.4014245348822247 msec\nrounds: 344"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 733139.6177356016,
            "unit": "iter/sec",
            "range": "stddev: 5.428565049639538e-7",
            "extra": "mean: 1.3639966737694955 usec\nrounds: 34875"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 684211.1814963811,
            "unit": "iter/sec",
            "range": "stddev: 4.6817643566371573e-7",
            "extra": "mean: 1.4615370620120292 usec\nrounds: 28857"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 200754.721544813,
            "unit": "iter/sec",
            "range": "stddev: 9.16851405849018e-7",
            "extra": "mean: 4.981202894282999 usec\nrounds: 42150"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 17982.195786637047,
            "unit": "iter/sec",
            "range": "stddev: 0.000008787366444304052",
            "extra": "mean: 55.61056123875158 usec\nrounds: 8173"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 224.2916245050468,
            "unit": "iter/sec",
            "range": "stddev: 0.00025539847247672343",
            "extra": "mean: 4.458481239354076 msec\nrounds: 188"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.045183640266116785,
            "unit": "iter/sec",
            "range": "stddev: 34.40945696486463",
            "extra": "mean: 22.131904249200126 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.034662910136118504,
            "unit": "iter/sec",
            "range": "stddev: 24.787212748042162",
            "extra": "mean: 28.849279996199947 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.2816754483680072,
            "unit": "iter/sec",
            "range": "stddev: 1.7589981955631218",
            "extra": "mean: 3.550185171600424 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.09800479649974742,
            "unit": "iter/sec",
            "range": "stddev: 4.5389312948004035",
            "extra": "mean: 10.203582229800123 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 97455.30789488251,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016341261578637016",
            "extra": "mean: 10.261113751532369 usec\nrounds: 13212"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.2828122457193803,
            "unit": "iter/sec",
            "range": "stddev: 1.8405200847072383",
            "extra": "mean: 3.535914781399697 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.21973042796701706,
            "unit": "iter/sec",
            "range": "stddev: 0.636710544401614",
            "extra": "mean: 4.551031048599725 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 5.854156917809972,
            "unit": "iter/sec",
            "range": "stddev: 0.01750739166797366",
            "extra": "mean: 170.81878980006877 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.4786246183694399,
            "unit": "iter/sec",
            "range": "stddev: 0.09874240521967113",
            "extra": "mean: 2.0893200257996796 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 4.5959657423466975,
            "unit": "iter/sec",
            "range": "stddev: 0.005326784269338288",
            "extra": "mean: 217.58212659988203 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 5.668754573725135,
            "unit": "iter/sec",
            "range": "stddev: 0.07355539933801572",
            "extra": "mean: 176.40559085677003 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 6.627266168108813,
            "unit": "iter/sec",
            "range": "stddev: 0.018453457681437",
            "extra": "mean: 150.8917817141732 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 1.1191396588626972,
            "unit": "iter/sec",
            "range": "stddev: 0.009023773927484246",
            "extra": "mean: 893.5435287998189 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 4.140409627603505,
            "unit": "iter/sec",
            "range": "stddev: 0.017122152616183384",
            "extra": "mean: 241.52199659984035 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 6.987365675958019,
            "unit": "iter/sec",
            "range": "stddev: 0.00847657046285531",
            "extra": "mean: 143.11545242877142 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 3.5071842779608833,
            "unit": "iter/sec",
            "range": "stddev: 0.09506977385334557",
            "extra": "mean: 285.12901539961604 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 6.911061548925925,
            "unit": "iter/sec",
            "range": "stddev: 0.006432992227535423",
            "extra": "mean: 144.695571428591 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 1.1054142655926549,
            "unit": "iter/sec",
            "range": "stddev: 0.015666207762160492",
            "extra": "mean: 904.6382258002268 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 5.16602061546474,
            "unit": "iter/sec",
            "range": "stddev: 0.07478768388833895",
            "extra": "mean: 193.57259183334463 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 3.165971028959601,
            "unit": "iter/sec",
            "range": "stddev: 0.14770418481655678",
            "extra": "mean: 315.8588599999348 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 6.965369874732142,
            "unit": "iter/sec",
            "range": "stddev: 0.006185647170682018",
            "extra": "mean: 143.5673938332608 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 7.284319444082283,
            "unit": "iter/sec",
            "range": "stddev: 0.004503970247926882",
            "extra": "mean: 137.2811842858417 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.9378904164642159,
            "unit": "iter/sec",
            "range": "stddev: 0.3448191559692869",
            "extra": "mean: 1.0662226444001135 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 5.066989297415462,
            "unit": "iter/sec",
            "range": "stddev: 0.03446475113757017",
            "extra": "mean: 197.35585399994306 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 6.614737515455132,
            "unit": "iter/sec",
            "range": "stddev: 0.010948936676720122",
            "extra": "mean: 151.1775785000585 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 6.665045483222647,
            "unit": "iter/sec",
            "range": "stddev: 0.0110505797892928",
            "extra": "mean: 150.03648549994372 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 4.018369439037777,
            "unit": "iter/sec",
            "range": "stddev: 0.08372994604628606",
            "extra": "mean: 248.85715839991462 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.698930921343447,
            "unit": "iter/sec",
            "range": "stddev: 0.07497041639886126",
            "extra": "mean: 1.4307565589999285 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 5.169139904982076,
            "unit": "iter/sec",
            "range": "stddev: 0.005020378827079316",
            "extra": "mean: 193.45578149977882 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.0873858431815773,
            "unit": "iter/sec",
            "range": "stddev: 0.1999680738942458",
            "extra": "mean: 919.6367657998053 msec\nrounds: 5"
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
          "id": "a7454d2189e332e77209e458170ba10d7bf46efb",
          "message": "Merge pull request #159 from iausathub/develop\n\nUpdate Starlink ephemeris data source and decayed sat check",
          "timestamp": "2025-07-18T11:51:08-07:00",
          "tree_id": "105fb1772633a401f295818f01c54a653cab11d9",
          "url": "https://github.com/iausathub/satchecker/commit/a7454d2189e332e77209e458170ba10d7bf46efb"
        },
        "date": 1752869092042,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 0.08106019594700926,
            "unit": "iter/sec",
            "range": "stddev: 26.978915531667006",
            "extra": "mean: 12.336511012799928 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 0.8397003851553173,
            "unit": "iter/sec",
            "range": "stddev: 0.9865422751273686",
            "extra": "mean: 1.1909009662000245 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 4.952899819676393,
            "unit": "iter/sec",
            "range": "stddev: 0.02055509524373245",
            "extra": "mean: 201.9019233999643 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 2267573.3587304363,
            "unit": "iter/sec",
            "range": "stddev: 4.044075345340456e-7",
            "extra": "mean: 441.0000656207558 nsec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 146564.61610982422,
            "unit": "iter/sec",
            "range": "stddev: 0.000001038999302664963",
            "extra": "mean: 6.822929207215179 usec\nrounds: 21287"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133280.40060709807,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010853199212748746",
            "extra": "mean: 7.50297864836057 usec\nrounds: 33160"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1441.3265050374107,
            "unit": "iter/sec",
            "range": "stddev: 0.00002012961204416065",
            "extra": "mean: 693.8053220453643 usec\nrounds: 857"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 744144.043515711,
            "unit": "iter/sec",
            "range": "stddev: 4.6863046473924655e-7",
            "extra": "mean: 1.3438258475811975 usec\nrounds: 75330"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 207962.72860569748,
            "unit": "iter/sec",
            "range": "stddev: 7.856293952712212e-7",
            "extra": "mean: 4.808553949568651 usec\nrounds: 48268"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 163153.93112611785,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010330317349781422",
            "extra": "mean: 6.129181154862893 usec\nrounds: 28495"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4281.061946515973,
            "unit": "iter/sec",
            "range": "stddev: 0.000012412261361705489",
            "extra": "mean: 233.5869026174272 usec\nrounds: 1643"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 681415.6252987067,
            "unit": "iter/sec",
            "range": "stddev: 4.973478657360991e-7",
            "extra": "mean: 1.4675331220378722 usec\nrounds: 88098"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 489.86171458821224,
            "unit": "iter/sec",
            "range": "stddev: 0.0001047222390277433",
            "extra": "mean: 2.0413924383550173 msec\nrounds: 292"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 773.8703300349199,
            "unit": "iter/sec",
            "range": "stddev: 0.000022427942802547496",
            "extra": "mean: 1.2922061502924866 msec\nrounds: 519"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.21221738778992308,
            "unit": "iter/sec",
            "range": "stddev: 2.731362278516882",
            "extra": "mean: 4.71214922779991 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 4.161100594730134,
            "unit": "iter/sec",
            "range": "stddev: 0.019163054832612332",
            "extra": "mean: 240.32103459994687 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 0.589884743369691,
            "unit": "iter/sec",
            "range": "stddev: 0.9873546030001423",
            "extra": "mean: 1.695246421000047 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.09889141933920591,
            "unit": "iter/sec",
            "range": "stddev: 1.4177622928890228",
            "extra": "mean: 10.112100793800073 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.1731144577476602,
            "unit": "iter/sec",
            "range": "stddev: 1.955322809335081",
            "extra": "mean: 5.776525040199976 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.027548107451294882,
            "unit": "iter/sec",
            "range": "stddev: 33.18459500942172",
            "extra": "mean: 36.30013429300006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 3.3872876452288274,
            "unit": "iter/sec",
            "range": "stddev: 0.029000646362049565",
            "extra": "mean: 295.221458800097 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.2863269005082904,
            "unit": "iter/sec",
            "range": "stddev: 1.2005622958311188",
            "extra": "mean: 3.492511525200007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.14924424000659442,
            "unit": "iter/sec",
            "range": "stddev: 1.4176839916811745",
            "extra": "mean: 6.700426093200076 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.05734544483787308,
            "unit": "iter/sec",
            "range": "stddev: 27.23141941536664",
            "extra": "mean: 17.43817669960008 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18518.554278872158,
            "unit": "iter/sec",
            "range": "stddev: 0.000004985661138580915",
            "extra": "mean: 53.999895723010155 usec\nrounds: 8487"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.24472530139612797,
            "unit": "iter/sec",
            "range": "stddev: 2.518234502515809",
            "extra": "mean: 4.086214193199976 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.486980860442904,
            "unit": "iter/sec",
            "range": "stddev: 0.08518600660829491",
            "extra": "mean: 2.053468793600041 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.4683037110415197,
            "unit": "iter/sec",
            "range": "stddev: 0.1064060190284733",
            "extra": "mean: 2.135366379600055 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.5720166624783634,
            "unit": "iter/sec",
            "range": "stddev: 0.06706479824632323",
            "extra": "mean: 1.7482008228000268 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.42172861343043344,
            "unit": "iter/sec",
            "range": "stddev: 0.12319480888600975",
            "extra": "mean: 2.3711931515999822 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.39929923517688476,
            "unit": "iter/sec",
            "range": "stddev: 0.042856204192276225",
            "extra": "mean: 2.50438746660011 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.40730666079576805,
            "unit": "iter/sec",
            "range": "stddev: 0.0462128640939998",
            "extra": "mean: 2.455152582200026 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.34738517199413543,
            "unit": "iter/sec",
            "range": "stddev: 0.05425319372781495",
            "extra": "mean: 2.8786490634000983 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.4708361805515145,
            "unit": "iter/sec",
            "range": "stddev: 0.09985387150474286",
            "extra": "mean: 2.1238809618000234 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.5177674282500938,
            "unit": "iter/sec",
            "range": "stddev: 0.07645501805394658",
            "extra": "mean: 1.9313690769999083 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.935073073941136,
            "unit": "iter/sec",
            "range": "stddev: 0.07113527773119337",
            "extra": "mean: 1.0694351359998109 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.15022177946293658,
            "unit": "iter/sec",
            "range": "stddev: 0.18777145119435526",
            "extra": "mean: 6.656824353799675 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 1.3425702730206752,
            "unit": "iter/sec",
            "range": "stddev: 0.07205051120204337",
            "extra": "mean: 744.8399685999902 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.10216618573324705,
            "unit": "iter/sec",
            "range": "stddev: 0.18641612793431053",
            "extra": "mean: 9.787974297200162 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.9115870819758856,
            "unit": "iter/sec",
            "range": "stddev: 0.06098186119940108",
            "extra": "mean: 1.0969879013999162 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.44419319195497686,
            "unit": "iter/sec",
            "range": "stddev: 0.09534247770807831",
            "extra": "mean: 2.2512726851999103 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.33131649321573325,
            "unit": "iter/sec",
            "range": "stddev: 0.05073001847509072",
            "extra": "mean: 3.0182620559999123 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.46021157315860073,
            "unit": "iter/sec",
            "range": "stddev: 0.12000185978011409",
            "extra": "mean: 2.172913629999857 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.16509695629024757,
            "unit": "iter/sec",
            "range": "stddev: 0.12795235763420618",
            "extra": "mean: 6.057046855800036 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.5601002633600012,
            "unit": "iter/sec",
            "range": "stddev: 0.0554126297502123",
            "extra": "mean: 1.785394625599838 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 1.820707069369414,
            "unit": "iter/sec",
            "range": "stddev: 0.03214294622545041",
            "extra": "mean: 549.2371709999134 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.9186895858419293,
            "unit": "iter/sec",
            "range": "stddev: 0.060954927348482554",
            "extra": "mean: 1.0885069509997265 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.7964983041666461,
            "unit": "iter/sec",
            "range": "stddev: 0.02454423627126524",
            "extra": "mean: 1.2554954540000836 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 227.661762672218,
            "unit": "iter/sec",
            "range": "stddev: 0.00011953694446432568",
            "extra": "mean: 4.392481145109011 msec\nrounds: 193"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 95041.97505097996,
            "unit": "iter/sec",
            "range": "stddev: 0.000001615966047654768",
            "extra": "mean: 10.521666868387424 usec\nrounds: 13445"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.6743501069463284,
            "unit": "iter/sec",
            "range": "stddev: 0.07842605991939773",
            "extra": "mean: 1.4829092331998255 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.19248330472467934,
            "unit": "iter/sec",
            "range": "stddev: 0.1012843035406016",
            "extra": "mean: 5.195255772599921 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.43600842024656156,
            "unit": "iter/sec",
            "range": "stddev: 0.12152012833133966",
            "extra": "mean: 2.2935336878001182 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.4452109684031559,
            "unit": "iter/sec",
            "range": "stddev: 0.17349784733299892",
            "extra": "mean: 2.2461261536001986 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 7.157248571884618,
            "unit": "iter/sec",
            "range": "stddev: 0.004469460117676415",
            "extra": "mean: 139.71849516701695 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.6265471127360598,
            "unit": "iter/sec",
            "range": "stddev: 0.042307713732200734",
            "extra": "mean: 1.5960491711997746 sec\nrounds: 5"
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
          "id": "a299dac16568ddca237cfd25c4afc1eba92a2b85",
          "message": "Merge pull request #161 from iausathub/develop\n\nFix filenames/path for Starlink ephemeris files",
          "timestamp": "2025-07-21T23:59:35-07:00",
          "tree_id": "11b372f20e6e355700fd6563ee26979841506543",
          "url": "https://github.com/iausathub/satchecker/commit/a299dac16568ddca237cfd25c4afc1eba92a2b85"
        },
        "date": 1753167865818,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 483.44845067190704,
            "unit": "iter/sec",
            "range": "stddev: 0.00009390675566745357",
            "extra": "mean: 2.0684728611916707 msec\nrounds: 353"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 99575.8070448115,
            "unit": "iter/sec",
            "range": "stddev: 0.000005187214023437433",
            "extra": "mean: 10.042600001725077 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1412.3317962314586,
            "unit": "iter/sec",
            "range": "stddev: 0.000018186798550371626",
            "extra": "mean: 708.0489178734853 usec\nrounds: 828"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4179.546487000414,
            "unit": "iter/sec",
            "range": "stddev: 0.000014361956940414933",
            "extra": "mean: 239.26040854200002 usec\nrounds: 1569"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 691641.1829973335,
            "unit": "iter/sec",
            "range": "stddev: 5.63288911075539e-7",
            "extra": "mean: 1.44583640272308 usec\nrounds: 34206"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133418.24253040788,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016342207566972336",
            "extra": "mean: 7.495226897266962 usec\nrounds: 18872"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 748.0934217901279,
            "unit": "iter/sec",
            "range": "stddev: 0.00003012815509853955",
            "extra": "mean: 1.3367314440582563 msec\nrounds: 286"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 144492.35236622312,
            "unit": "iter/sec",
            "range": "stddev: 0.0000014300770937826513",
            "extra": "mean: 6.9207815058990105 usec\nrounds: 18362"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 743355.3433233864,
            "unit": "iter/sec",
            "range": "stddev: 4.1347182747420316e-7",
            "extra": "mean: 1.3452516471183336 usec\nrounds: 36428"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12566568.350123562,
            "unit": "iter/sec",
            "range": "stddev: 9.348419211385319e-9",
            "extra": "mean: 79.57621938928897 nsec\nrounds: 67214"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 200644.1410375455,
            "unit": "iter/sec",
            "range": "stddev: 9.065422750084614e-7",
            "extra": "mean: 4.983948172266217 usec\nrounds: 34730"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18248.907028856724,
            "unit": "iter/sec",
            "range": "stddev: 0.000005602939200906689",
            "extra": "mean: 54.79780232420028 usec\nrounds: 8433"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 94794.81350984513,
            "unit": "iter/sec",
            "range": "stddev: 0.0000020887915738391797",
            "extra": "mean: 10.549100346045226 usec\nrounds: 9248"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 223.2387286904821,
            "unit": "iter/sec",
            "range": "stddev: 0.0001143377460397053",
            "extra": "mean: 4.479509473405434 msec\nrounds: 188"
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
          "id": "67f961027098c1b28b58ad9fd241f18a45ce45a8",
          "message": "Update CONTRIBUTING.md",
          "timestamp": "2025-08-02T21:31:55-07:00",
          "tree_id": "02dfbb87ed23386a49c1269c7fd6321ee6ab0cb6",
          "url": "https://github.com/iausathub/satchecker/commit/67f961027098c1b28b58ad9fd241f18a45ce45a8"
        },
        "date": 1754196794064,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1413.138577135357,
            "unit": "iter/sec",
            "range": "stddev: 0.000021830409892137335",
            "extra": "mean: 707.6446826801299 usec\nrounds: 791"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 694.8251507254946,
            "unit": "iter/sec",
            "range": "stddev: 0.00013301781295042402",
            "extra": "mean: 1.4392109999988634 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 147111.51993168567,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010518446076156186",
            "extra": "mean: 6.797564191195707 usec\nrounds: 25463"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133796.62524135527,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010757702940470385",
            "extra": "mean: 7.474030067620192 usec\nrounds: 18791"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 205867.4345263733,
            "unit": "iter/sec",
            "range": "stddev: 7.665976377496864e-7",
            "extra": "mean: 4.857494835453889 usec\nrounds: 43663"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12453320.572024582,
            "unit": "iter/sec",
            "range": "stddev: 8.2790338067336e-9",
            "extra": "mean: 80.29986815299122 nsec\nrounds: 64772"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4104.88966114789,
            "unit": "iter/sec",
            "range": "stddev: 0.000012897860121805321",
            "extra": "mean: 243.61190739542565 usec\nrounds: 1555"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 730950.9093560653,
            "unit": "iter/sec",
            "range": "stddev: 4.4825488124732703e-7",
            "extra": "mean: 1.3680809301967416 usec\nrounds: 62696"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 162240.02202004218,
            "unit": "iter/sec",
            "range": "stddev: 0.000001093678111814349",
            "extra": "mean: 6.163707250215153 usec\nrounds: 31737"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 674996.0302325997,
            "unit": "iter/sec",
            "range": "stddev: 5.371298758519517e-7",
            "extra": "mean: 1.4814901943281145 usec\nrounds: 44719"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 428.06424298934644,
            "unit": "iter/sec",
            "range": "stddev: 0.0041422736577990775",
            "extra": "mean: 2.336097948795241 msec\nrounds: 332"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 1.932127579379505,
            "unit": "iter/sec",
            "range": "stddev: 0.09432894032137337",
            "extra": "mean: 517.5641663999983 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.3143624551009861,
            "unit": "iter/sec",
            "range": "stddev: 0.6720271341535462",
            "extra": "mean: 3.1810414499999977 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 0.6966425799345806,
            "unit": "iter/sec",
            "range": "stddev: 0.2572084061791875",
            "extra": "mean: 1.435456328400005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.10984167613727507,
            "unit": "iter/sec",
            "range": "stddev: 3.706965232686005",
            "extra": "mean: 9.10401256759999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.21631678931415785,
            "unit": "iter/sec",
            "range": "stddev: 1.2379869565725945",
            "extra": "mean: 4.622849678799992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.0704033710725524,
            "unit": "iter/sec",
            "range": "stddev: 0.9790189422885062",
            "extra": "mean: 14.203865308799994 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.1935981660589456,
            "unit": "iter/sec",
            "range": "stddev: 2.6265878047817006",
            "extra": "mean: 5.165338186600001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 224.32785106459306,
            "unit": "iter/sec",
            "range": "stddev: 0.00008355163539687695",
            "extra": "mean: 4.457761242103013 msec\nrounds: 190"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.06455928691306037,
            "unit": "iter/sec",
            "range": "stddev: 4.176579068592336",
            "extra": "mean: 15.4896382506 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.07991007346987582,
            "unit": "iter/sec",
            "range": "stddev: 2.947022502370407",
            "extra": "mean: 12.514066832599974 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18421.571758993105,
            "unit": "iter/sec",
            "range": "stddev: 0.0000055548431825593195",
            "extra": "mean: 54.2841844921195 usec\nrounds: 9144"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 90165.59096238048,
            "unit": "iter/sec",
            "range": "stddev: 0.000002877032639007286",
            "extra": "mean: 11.09070532701579 usec\nrounds: 13666"
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
          "id": "f1f1cb2113ba82f3d677562a8f9b1723dbda6207",
          "message": "Update README.md",
          "timestamp": "2025-08-02T21:32:15-07:00",
          "tree_id": "1008012eaf41acfcc1c00edd83c467c545707cf4",
          "url": "https://github.com/iausathub/satchecker/commit/f1f1cb2113ba82f3d677562a8f9b1723dbda6207"
        },
        "date": 1754197178365,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 143151.2040419306,
            "unit": "iter/sec",
            "range": "stddev: 0.000001030088449493285",
            "extra": "mean: 6.985620600907336 usec\nrounds: 11650"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 201896.27734051313,
            "unit": "iter/sec",
            "range": "stddev: 7.40971445720529e-7",
            "extra": "mean: 4.953038328257164 usec\nrounds: 51346"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 2105263.175806895,
            "unit": "iter/sec",
            "range": "stddev: 5.247918699118233e-7",
            "extra": "mean: 474.99999595856934 nsec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1415.3590483867026,
            "unit": "iter/sec",
            "range": "stddev: 0.000021335011070918018",
            "extra": "mean: 706.534501715201 usec\nrounds: 875"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 679014.192419332,
            "unit": "iter/sec",
            "range": "stddev: 4.810934013765006e-7",
            "extra": "mean: 1.472723267295774 usec\nrounds: 42420"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4179.747401707529,
            "unit": "iter/sec",
            "range": "stddev: 0.00001268227857013576",
            "extra": "mean: 239.24890762333519 usec\nrounds: 1548"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 484.1746653511593,
            "unit": "iter/sec",
            "range": "stddev: 0.00012048681557553026",
            "extra": "mean: 2.0653703540533788 msec\nrounds: 370"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 160819.9165844457,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010184918930180261",
            "extra": "mean: 6.218135298403201 usec\nrounds: 33962"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 131373.8177776492,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011201970508698103",
            "extra": "mean: 7.611866785301958 usec\nrounds: 27527"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 762.3192754726457,
            "unit": "iter/sec",
            "range": "stddev: 0.000024355424061823376",
            "extra": "mean: 1.3117863238863925 msec\nrounds: 494"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 719729.3435830226,
            "unit": "iter/sec",
            "range": "stddev: 4.460584081884014e-7",
            "extra": "mean: 1.3894111847958128 usec\nrounds: 74047"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.1327884486994912,
            "unit": "iter/sec",
            "range": "stddev: 2.3660792137820095",
            "extra": "mean: 7.530775528999999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.14345125246139037,
            "unit": "iter/sec",
            "range": "stddev: 1.3824712536916628",
            "extra": "mean: 6.971009195400006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.09601880780273445,
            "unit": "iter/sec",
            "range": "stddev: 1.5514792538593944",
            "extra": "mean: 10.414626289199997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.1629209261456656,
            "unit": "iter/sec",
            "range": "stddev: 1.5934866695433965",
            "extra": "mean: 6.13794693939999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.06667224728399902,
            "unit": "iter/sec",
            "range": "stddev: 2.0790909303414704",
            "extra": "mean: 14.998744466200026 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.06712473124202052,
            "unit": "iter/sec",
            "range": "stddev: 1.3095694702161476",
            "extra": "mean: 14.897638791200006 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18540.993620012185,
            "unit": "iter/sec",
            "range": "stddev: 0.000007008966063662458",
            "extra": "mean: 53.934542047447344 usec\nrounds: 5684"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 95672.5474750424,
            "unit": "iter/sec",
            "range": "stddev: 0.000001634443411306412",
            "extra": "mean: 10.452319148926861 usec\nrounds: 13489"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 228.64813028629274,
            "unit": "iter/sec",
            "range": "stddev: 0.00009783474619349496",
            "extra": "mean: 4.373532373730279 msec\nrounds: 198"
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
          "id": "43656f5d7bed303f7077bc7944e0e8ef8fb3a4d9",
          "message": "Update README.md",
          "timestamp": "2025-08-02T21:29:29-07:00",
          "tree_id": "72d41524e99baf14ef5f95e515fab9b9d12c7c65",
          "url": "https://github.com/iausathub/satchecker/commit/43656f5d7bed303f7077bc7944e0e8ef8fb3a4d9"
        },
        "date": 1754198955511,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.0859835176821971,
            "unit": "iter/sec",
            "range": "stddev: 0.7835144055274867",
            "extra": "mean: 11.630135948799989 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.2042813655647827,
            "unit": "iter/sec",
            "range": "stddev: 0.20501466411626404",
            "extra": "mean: 4.895209101599994 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.059005870794826505,
            "unit": "iter/sec",
            "range": "stddev: 3.6850302326648565",
            "extra": "mean: 16.9474661848 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.30918817511481755,
            "unit": "iter/sec",
            "range": "stddev: 0.4024719286755883",
            "extra": "mean: 3.2342763419999754 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.04567109063188133,
            "unit": "iter/sec",
            "range": "stddev: 1.0455692710678286",
            "extra": "mean: 21.895689070799996 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.3683807726137688,
            "unit": "iter/sec",
            "range": "stddev: 0.37763697835811916",
            "extra": "mean: 2.714582503600036 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 2.7124093263193547,
            "unit": "iter/sec",
            "range": "stddev: 0.14888725843622108",
            "extra": "mean: 368.67591860000175 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 224.88339820811856,
            "unit": "iter/sec",
            "range": "stddev: 0.00009420965650313792",
            "extra": "mean: 4.446748883946289 msec\nrounds: 181"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 89829.0907937283,
            "unit": "iter/sec",
            "range": "stddev: 0.000003124729680398897",
            "extra": "mean: 11.132251157882344 usec\nrounds: 13581"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18472.90369948883,
            "unit": "iter/sec",
            "range": "stddev: 0.000005416039146935054",
            "extra": "mean: 54.13334125850888 usec\nrounds: 9339"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1432.6398198199417,
            "unit": "iter/sec",
            "range": "stddev: 0.00002309223406114236",
            "extra": "mean: 698.0121494359154 usec\nrounds: 890"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 115019.20813810611,
            "unit": "iter/sec",
            "range": "stddev: 0.0000029426480231687262",
            "extra": "mean: 8.694200005265884 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 753.8373510758078,
            "unit": "iter/sec",
            "range": "stddev: 0.00003470879919768709",
            "extra": "mean: 1.3265461025152063 msec\nrounds: 556"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 737731.585701192,
            "unit": "iter/sec",
            "range": "stddev: 4.625169570807221e-7",
            "extra": "mean: 1.355506554663143 usec\nrounds: 60347"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_full_satellite_position_calculation",
            "value": 4180.729595949695,
            "unit": "iter/sec",
            "range": "stddev: 0.000014349780884551978",
            "extra": "mean: 239.19269999399228 usec\nrounds: 1620"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12448716.318655873,
            "unit": "iter/sec",
            "range": "stddev: 1.1958034071489862e-8",
            "extra": "mean: 80.32956767609804 nsec\nrounds: 64604"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 144309.41567083995,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010792125101775561",
            "extra": "mean: 6.929554771955647 usec\nrounds: 21699"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 690265.4956035266,
            "unit": "iter/sec",
            "range": "stddev: 4.111456710597129e-7",
            "extra": "mean: 1.448717930085235 usec\nrounds: 48977"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 489.5532189318034,
            "unit": "iter/sec",
            "range": "stddev: 0.00006807210793936916",
            "extra": "mean: 2.0426788372099414 msec\nrounds: 387"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 135835.18396585394,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011028558139816597",
            "extra": "mean: 7.361862890040172 usec\nrounds: 25308"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 204286.30388636462,
            "unit": "iter/sec",
            "range": "stddev: 7.8223001157367e-7",
            "extra": "mean: 4.895090767104267 usec\nrounds: 49931"
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
          "id": "a24ed917b7bb00e62eef6341b522424071e89a6f",
          "message": "Merge pull request #165 from iausathub/develop\n\nFOV query illuminated-only filter; solar position and satellite altitude in ephemeris results",
          "timestamp": "2025-08-28T10:13:40-07:00",
          "tree_id": "d1bbbf046103498c6accea66bbfa3cd9693b5ab0",
          "url": "https://github.com/iausathub/satchecker/commit/a24ed917b7bb00e62eef6341b522424071e89a6f"
        },
        "date": 1756404817531,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 0.27261380248599903,
            "unit": "iter/sec",
            "range": "stddev: 7.181636537084533",
            "extra": "mean: 3.668192846000005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 0.22659923722890782,
            "unit": "iter/sec",
            "range": "stddev: 9.345430914143066",
            "extra": "mean: 4.413077520600001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.0545288575831893,
            "unit": "iter/sec",
            "range": "stddev: 0.12207784351686046",
            "extra": "mean: 486.7295956000021 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 4.8297042000620465,
            "unit": "iter/sec",
            "range": "stddev: 0.006379393210002107",
            "extra": "mean: 207.0520178000038 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 2.7242437545649483,
            "unit": "iter/sec",
            "range": "stddev: 0.05329007304778235",
            "extra": "mean: 367.0743479999999 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.6616794609973309,
            "unit": "iter/sec",
            "range": "stddev: 0.047092615921721384",
            "extra": "mean: 1.5113057891999973 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 4.70882389872471,
            "unit": "iter/sec",
            "range": "stddev: 0.013116478483228416",
            "extra": "mean: 212.36725380000507 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 5.318261273101867,
            "unit": "iter/sec",
            "range": "stddev: 0.005974614987201913",
            "extra": "mean: 188.03137880000236 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.0675572771150597,
            "unit": "iter/sec",
            "range": "stddev: 0.05567747137469444",
            "extra": "mean: 325.99228299999936 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 4.322378590415062,
            "unit": "iter/sec",
            "range": "stddev: 0.085525709789883",
            "extra": "mean: 231.35409800000275 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.669407297167736,
            "unit": "iter/sec",
            "range": "stddev: 0.03193724682169155",
            "extra": "mean: 1.493858827400004 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 4.666389680352473,
            "unit": "iter/sec",
            "range": "stddev: 0.01107198023592",
            "extra": "mean: 214.29843379999625 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.061848921692825,
            "unit": "iter/sec",
            "range": "stddev: 0.11179958981333694",
            "extra": "mean: 485.00158740000074 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 5.433639959492422,
            "unit": "iter/sec",
            "range": "stddev: 0.005611201343407156",
            "extra": "mean: 184.03869366666945 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 3.238658604424995,
            "unit": "iter/sec",
            "range": "stddev: 0.04792127998897358",
            "extra": "mean: 308.7698094000075 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.6744872927775108,
            "unit": "iter/sec",
            "range": "stddev: 0.012202287862649751",
            "extra": "mean: 1.4826076201999911 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 5.4595354799002775,
            "unit": "iter/sec",
            "range": "stddev: 0.00401390637111742",
            "extra": "mean: 183.16576633334117 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 5.228267355230718,
            "unit": "iter/sec",
            "range": "stddev: 0.008092793539245772",
            "extra": "mean: 191.2679540000056 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.19528919502659886,
            "unit": "iter/sec",
            "range": "stddev: 0.276149594089807",
            "extra": "mean: 5.120610998799998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.6551257322533263,
            "unit": "iter/sec",
            "range": "stddev: 0.038559596213309566",
            "extra": "mean: 1.5264245483999956 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.23708525890019275,
            "unit": "iter/sec",
            "range": "stddev: 0.058786352002583385",
            "extra": "mean: 4.2178919290000065 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.05943381500881137,
            "unit": "iter/sec",
            "range": "stddev: 0.9578399024300838",
            "extra": "mean: 16.825438512600023 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.07626568500682948,
            "unit": "iter/sec",
            "range": "stddev: 0.07801317977714775",
            "extra": "mean: 13.112056882599973 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.2689084378932758,
            "unit": "iter/sec",
            "range": "stddev: 0.0929375314355363",
            "extra": "mean: 3.718737901400027 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.1977350789720403,
            "unit": "iter/sec",
            "range": "stddev: 0.4835448511020989",
            "extra": "mean: 5.057271604000016 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.18480266955894945,
            "unit": "iter/sec",
            "range": "stddev: 0.3529784838326097",
            "extra": "mean: 5.411177243200018 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 220.95591339838407,
            "unit": "iter/sec",
            "range": "stddev: 0.0001909458085351945",
            "extra": "mean: 4.525789713520803 msec\nrounds: 185"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.2980642476987494,
            "unit": "iter/sec",
            "range": "stddev: 0.18834565860292624",
            "extra": "mean: 3.3549813764000644 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.282561463867088,
            "unit": "iter/sec",
            "range": "stddev: 0.25758698058701257",
            "extra": "mean: 3.5390530128000135 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 5.556538433115967,
            "unit": "iter/sec",
            "range": "stddev: 0.012984186040372664",
            "extra": "mean: 179.96816040003978 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.13159834472894247,
            "unit": "iter/sec",
            "range": "stddev: 3.0886172341643956",
            "extra": "mean: 7.598879773599992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.1722205640535431,
            "unit": "iter/sec",
            "range": "stddev: 0.13668411382989634",
            "extra": "mean: 5.8065075184000765 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.1253679554821557,
            "unit": "iter/sec",
            "range": "stddev: 1.1546154099785975",
            "extra": "mean: 7.976519965999887 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18396.00454446813,
            "unit": "iter/sec",
            "range": "stddev: 0.000005670656211327168",
            "extra": "mean: 54.35962997197184 usec\nrounds: 8529"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.8578492966759097,
            "unit": "iter/sec",
            "range": "stddev: 0.08237579025603452",
            "extra": "mean: 1.1657059158000265 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.42700786839020205,
            "unit": "iter/sec",
            "range": "stddev: 0.056880636846933404",
            "extra": "mean: 2.341877220600054 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.27571240670366554,
            "unit": "iter/sec",
            "range": "stddev: 0.06646004054165687",
            "extra": "mean: 3.6269677232000506 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.11217514348648298,
            "unit": "iter/sec",
            "range": "stddev: 1.025214047476389",
            "extra": "mean: 8.914630896999915 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.3573867055638333,
            "unit": "iter/sec",
            "range": "stddev: 0.07172449326239437",
            "extra": "mean: 2.798089532799895 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.06316576652541282,
            "unit": "iter/sec",
            "range": "stddev: 2.079559304476539",
            "extra": "mean: 15.831360165599836 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.37920563599140594,
            "unit": "iter/sec",
            "range": "stddev: 0.09372597536150382",
            "extra": "mean: 2.637091606999911 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.0884544881991423,
            "unit": "iter/sec",
            "range": "stddev: 3.2077073594034604",
            "extra": "mean: 11.30524883879998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.04634183677844763,
            "unit": "iter/sec",
            "range": "stddev: 0.11191423054600726",
            "extra": "mean: 21.578773512600037 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.2283464274217759,
            "unit": "iter/sec",
            "range": "stddev: 0.16528734659040925",
            "extra": "mean: 4.379310906200044 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 93252.11926642191,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016272815638373694",
            "extra": "mean: 10.723616877199257 usec\nrounds: 13142"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.14571305741224466,
            "unit": "iter/sec",
            "range": "stddev: 0.39562649415365564",
            "extra": "mean: 6.862802948200079 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.0629524331011334,
            "unit": "iter/sec",
            "range": "stddev: 0.3785270668344696",
            "extra": "mean: 15.885009533999982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.23551165763729603,
            "unit": "iter/sec",
            "range": "stddev: 0.15681687306753853",
            "extra": "mean: 4.246074313400095 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.2909325613761453,
            "unit": "iter/sec",
            "range": "stddev: 0.07616420391741102",
            "extra": "mean: 3.437222685800043 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.3599307640436009,
            "unit": "iter/sec",
            "range": "stddev: 0.13051701408342434",
            "extra": "mean: 2.7783121086000393 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.14684988736688528,
            "unit": "iter/sec",
            "range": "stddev: 0.19489668443527947",
            "extra": "mean: 6.809674954000002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 4.471084149430754,
            "unit": "iter/sec",
            "range": "stddev: 0.032911537796369725",
            "extra": "mean: 223.65940040008354 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.1457822229667281,
            "unit": "iter/sec",
            "range": "stddev: 0.18145677045004185",
            "extra": "mean: 6.859546930000033 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 3.7774076907090515,
            "unit": "iter/sec",
            "range": "stddev: 0.008706413474672367",
            "extra": "mean: 264.73181659994225 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.64767830518999,
            "unit": "iter/sec",
            "range": "stddev: 0.04726297716988355",
            "extra": "mean: 1.5439763722001771 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.0633670390846888,
            "unit": "iter/sec",
            "range": "stddev: 0.048435356368318354",
            "extra": "mean: 940.4090621999785 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 108304.81478969299,
            "unit": "iter/sec",
            "range": "stddev: 0.0000032722485913660715",
            "extra": "mean: 9.233199853042606 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 483.904600276967,
            "unit": "iter/sec",
            "range": "stddev: 0.00009450807771775944",
            "extra": "mean: 2.066523028356501 msec\nrounds: 388"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12616288.685818054,
            "unit": "iter/sec",
            "range": "stddev: 8.72251945596329e-9",
            "extra": "mean: 79.2626123975858 nsec\nrounds: 111396"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 524.7377078236127,
            "unit": "iter/sec",
            "range": "stddev: 0.00005219047516768003",
            "extra": "mean: 1.9057140073801286 msec\nrounds: 406"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 745926.2317624121,
            "unit": "iter/sec",
            "range": "stddev: 4.2029068315922923e-7",
            "extra": "mean: 1.3406151405042879 usec\nrounds: 46664"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1406.7712746948825,
            "unit": "iter/sec",
            "range": "stddev: 0.00001653955794596181",
            "extra": "mean: 710.8476111135351 usec\nrounds: 774"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 143628.89511497886,
            "unit": "iter/sec",
            "range": "stddev: 0.000001088639209035746",
            "extra": "mean: 6.962387332990848 usec\nrounds: 21031"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 129435.81386510692,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010392619036070223",
            "extra": "mean: 7.725837000894991 usec\nrounds: 23025"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 697893.2109002679,
            "unit": "iter/sec",
            "range": "stddev: 4.0520678207710566e-7",
            "extra": "mean: 1.4328839776360922 usec\nrounds: 53119"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 202736.75657465067,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011736938872916763",
            "extra": "mean: 4.932504676978914 usec\nrounds: 34840"
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
          "id": "f06d3996fbd3c381fdc259083b1f336fccf64635",
          "message": "Merge pull request #166 from iausathub/dependabot/pip/src/api/tornado-6.5\n\nBump tornado from 6.4.2 to 6.5 in /src/api",
          "timestamp": "2025-09-02T10:18:28-07:00",
          "tree_id": "ff7a7be1e706a377d18e3cc92e26b2bd1c565ea8",
          "url": "https://github.com/iausathub/satchecker/commit/f06d3996fbd3c381fdc259083b1f336fccf64635"
        },
        "date": 1756837426132,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 0.294172288246242,
            "unit": "iter/sec",
            "range": "stddev: 6.874378542613218",
            "extra": "mean: 3.399368465200001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 5.008786157228881,
            "unit": "iter/sec",
            "range": "stddev: 0.025687603956141614",
            "extra": "mean: 199.64917020000144 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.7228338025780278,
            "unit": "iter/sec",
            "range": "stddev: 0.06311173764041735",
            "extra": "mean: 1.3834438793999992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 4.7851947971739754,
            "unit": "iter/sec",
            "range": "stddev: 0.010799172852753555",
            "extra": "mean: 208.97790840000425 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 3.671781744546122,
            "unit": "iter/sec",
            "range": "stddev: 0.04632395375041868",
            "extra": "mean: 272.3473424000076 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.4470979800451658,
            "unit": "iter/sec",
            "range": "stddev: 0.10738402043670085",
            "extra": "mean: 408.6473071999933 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 5.253769160384446,
            "unit": "iter/sec",
            "range": "stddev: 0.015186911961084003",
            "extra": "mean: 190.33953900000142 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.484456800988634,
            "unit": "iter/sec",
            "range": "stddev: 0.1216977371916795",
            "extra": "mean: 402.5024703999975 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.7403818973785997,
            "unit": "iter/sec",
            "range": "stddev: 0.039787753133022054",
            "extra": "mean: 1.350654308999998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 5.5078984792635834,
            "unit": "iter/sec",
            "range": "stddev: 0.014069677126159561",
            "extra": "mean: 181.5574494999955 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 5.815176382775276,
            "unit": "iter/sec",
            "range": "stddev: 0.014578366591781657",
            "extra": "mean: 171.963829500001 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.7273160841978267,
            "unit": "iter/sec",
            "range": "stddev: 0.0462437693407508",
            "extra": "mean: 1.374918033199998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 5.144461081757462,
            "unit": "iter/sec",
            "range": "stddev: 0.02715464137455556",
            "extra": "mean: 194.38382059999526 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 5.881639137542813,
            "unit": "iter/sec",
            "range": "stddev: 0.004862555726436433",
            "extra": "mean: 170.02063142856676 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.6149345697673927,
            "unit": "iter/sec",
            "range": "stddev: 0.05134981965204695",
            "extra": "mean: 276.6301798000029 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 5.83292033664953,
            "unit": "iter/sec",
            "range": "stddev: 0.009931335323928646",
            "extra": "mean: 171.44070933332975 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.7412969903493707,
            "unit": "iter/sec",
            "range": "stddev: 0.1075152957573327",
            "extra": "mean: 364.79082840000956 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 5.43773501805782,
            "unit": "iter/sec",
            "range": "stddev: 0.013141289170760722",
            "extra": "mean: 183.90009750000047 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 4.7284988676080975,
            "unit": "iter/sec",
            "range": "stddev: 0.011063964344803556",
            "extra": "mean: 211.4836078000053 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 0.9614714124050144,
            "unit": "iter/sec",
            "range": "stddev: 0.32872770465461487",
            "extra": "mean: 1.0400725254000123 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.7113418583202975,
            "unit": "iter/sec",
            "range": "stddev: 0.06779128102332369",
            "extra": "mean: 1.405793836400005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 145641.31208792172,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013820590352285653",
            "extra": "mean: 6.866183678682551 usec\nrounds: 11335"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 204903.38061382694,
            "unit": "iter/sec",
            "range": "stddev: 7.057467866031971e-7",
            "extra": "mean: 4.880348957661461 usec\nrounds: 60526"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 732956.4141931471,
            "unit": "iter/sec",
            "range": "stddev: 4.795455577915487e-7",
            "extra": "mean: 1.3643376067604507 usec\nrounds: 44540"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 482.7188492951573,
            "unit": "iter/sec",
            "range": "stddev: 0.00010493536370282614",
            "extra": "mean: 2.071599237237476 msec\nrounds: 333"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1420.8125389135969,
            "unit": "iter/sec",
            "range": "stddev: 0.00001813968830596557",
            "extra": "mean: 703.8226174190686 usec\nrounds: 907"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 679630.8492294146,
            "unit": "iter/sec",
            "range": "stddev: 3.462653619781881e-7",
            "extra": "mean: 1.4713870053630282 usec\nrounds: 67304"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 119135.55244738514,
            "unit": "iter/sec",
            "range": "stddev: 0.0000023736905055835756",
            "extra": "mean: 8.393799998884788 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 528.4924637942385,
            "unit": "iter/sec",
            "range": "stddev: 0.00008308474307237194",
            "extra": "mean: 1.8921745691899532 msec\nrounds: 383"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 132669.5630251787,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011089473936690533",
            "extra": "mean: 7.537523884134712 usec\nrounds: 28806"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12502719.952071888,
            "unit": "iter/sec",
            "range": "stddev: 8.8379812860869e-9",
            "extra": "mean: 79.98259609378114 nsec\nrounds: 65067"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.4128631847046579,
            "unit": "iter/sec",
            "range": "stddev: 0.09192239163205285",
            "extra": "mean: 2.4221098829999845 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.14993657408232494,
            "unit": "iter/sec",
            "range": "stddev: 8.214910341604751",
            "extra": "mean: 6.669486788800009 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.2655685946189276,
            "unit": "iter/sec",
            "range": "stddev: 0.6726162597220302",
            "extra": "mean: 3.7655054862000155 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 1.1546792086192097,
            "unit": "iter/sec",
            "range": "stddev: 0.16133950328613011",
            "extra": "mean: 866.0414013999798 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.11417619901750521,
            "unit": "iter/sec",
            "range": "stddev: 3.827224330662035",
            "extra": "mean: 8.758392805199993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.18845441519747794,
            "unit": "iter/sec",
            "range": "stddev: 0.558908660866681",
            "extra": "mean: 5.3063230116000115 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.17982533538200543,
            "unit": "iter/sec",
            "range": "stddev: 0.2076039103867988",
            "extra": "mean: 5.560951675000001 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18462.794104920373,
            "unit": "iter/sec",
            "range": "stddev: 0.000005395819500375778",
            "extra": "mean: 54.162982824658044 usec\nrounds: 8617"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 219.7703411731655,
            "unit": "iter/sec",
            "range": "stddev: 0.00022820339616985613",
            "extra": "mean: 4.550204521055284 msec\nrounds: 190"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 1.194877834786843,
            "unit": "iter/sec",
            "range": "stddev: 0.04439861263112869",
            "extra": "mean: 836.9056408000006 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.1801028152148755,
            "unit": "iter/sec",
            "range": "stddev: 0.07173585402898376",
            "extra": "mean: 5.55238405800003 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.2997382451308193,
            "unit": "iter/sec",
            "range": "stddev: 1.466678920535767",
            "extra": "mean: 3.3362442605999605 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.3012231708269931,
            "unit": "iter/sec",
            "range": "stddev: 0.21099758389393675",
            "extra": "mean: 3.3197977342000287 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.15811836941413387,
            "unit": "iter/sec",
            "range": "stddev: 1.2613752647458787",
            "extra": "mean: 6.3243758692000025 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 7.019150550598759,
            "unit": "iter/sec",
            "range": "stddev: 0.0033215219216909267",
            "extra": "mean: 142.4673815999995 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.649624007420843,
            "unit": "iter/sec",
            "range": "stddev: 0.22818024237320697",
            "extra": "mean: 1.5393519767999806 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 92824.09516872681,
            "unit": "iter/sec",
            "range": "stddev: 0.0000015335346290899858",
            "extra": "mean: 10.773064883447505 usec\nrounds: 13193"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.15581909918756923,
            "unit": "iter/sec",
            "range": "stddev: 1.344994504809718",
            "extra": "mean: 6.417698505599992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.42746913940324616,
            "unit": "iter/sec",
            "range": "stddev: 0.3181634130928581",
            "extra": "mean: 2.33935016079995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.5329856817535722,
            "unit": "iter/sec",
            "range": "stddev: 0.22319577849218508",
            "extra": "mean: 1.8762230098000146 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.436359685566213,
            "unit": "iter/sec",
            "range": "stddev: 0.08563855988478129",
            "extra": "mean: 2.2916874154000197 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.3532906499355893,
            "unit": "iter/sec",
            "range": "stddev: 0.12148366988268611",
            "extra": "mean: 2.8305306131999712 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.3871305891463727,
            "unit": "iter/sec",
            "range": "stddev: 0.11756375733719733",
            "extra": "mean: 2.5831076852000026 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.13631608997320502,
            "unit": "iter/sec",
            "range": "stddev: 1.5285455212206729",
            "extra": "mean: 7.335891164400072 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.09228736422335904,
            "unit": "iter/sec",
            "range": "stddev: 0.2610069143201844",
            "extra": "mean: 10.835719585400057 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.5031039397530521,
            "unit": "iter/sec",
            "range": "stddev: 0.05562177972046814",
            "extra": "mean: 1.98766084100007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.19262754808420865,
            "unit": "iter/sec",
            "range": "stddev: 3.5426785723228282",
            "extra": "mean: 5.191365461199984 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.3521153231204734,
            "unit": "iter/sec",
            "range": "stddev: 0.048433508131539335",
            "extra": "mean: 2.839978650000012 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 5.462569756976521,
            "unit": "iter/sec",
            "range": "stddev: 0.016252768797657583",
            "extra": "mean: 183.06402379994324 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.07471405410465408,
            "unit": "iter/sec",
            "range": "stddev: 24.34645721364499",
            "extra": "mean: 13.38436271440005 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.18158711456562687,
            "unit": "iter/sec",
            "range": "stddev: 4.681589372034652",
            "extra": "mean: 5.5069986787999365 sec\nrounds: 5"
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
          "id": "f03e3756a25a4bc04c92177e7e80afe32539e842",
          "message": "Update data directory for output in benchmark.yml",
          "timestamp": "2025-09-05T12:55:58-07:00",
          "tree_id": "58cbda84aebe52554f21b51b2865ea8012a38a0b",
          "url": "https://github.com/iausathub/satchecker/commit/f03e3756a25a4bc04c92177e7e80afe32539e842"
        },
        "date": 1757102533218,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 199489.04694084873,
            "unit": "iter/sec",
            "range": "stddev: 8.956508574503696e-7",
            "extra": "mean: 5.012806544193446 usec\nrounds: 30989"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1383.5801134433057,
            "unit": "iter/sec",
            "range": "stddev: 0.00002535992805435359",
            "extra": "mean: 722.7626288378107 usec\nrounds: 749"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 128635.71676017057,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011232201875797027",
            "extra": "mean: 7.773890682821846 usec\nrounds: 18890"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 666996.6147502161,
            "unit": "iter/sec",
            "range": "stddev: 5.326160352076195e-7",
            "extra": "mean: 1.4992579840521236 usec\nrounds: 36886"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 140421.22041659337,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011257991491718332",
            "extra": "mean: 7.121430771170192 usec\nrounds: 17536"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12366919.82821347,
            "unit": "iter/sec",
            "range": "stddev: 1.0667734247689692e-8",
            "extra": "mean: 80.86087836672091 nsec\nrounds: 67079"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 517.6986064352581,
            "unit": "iter/sec",
            "range": "stddev: 0.0000521239421480994",
            "extra": "mean: 1.9316258293329156 msec\nrounds: 375"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 726056.2722890137,
            "unit": "iter/sec",
            "range": "stddev: 4.682159882873724e-7",
            "extra": "mean: 1.3773037134536874 usec\nrounds: 68321"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 472.7924233884018,
            "unit": "iter/sec",
            "range": "stddev: 0.0001432927933792196",
            "extra": "mean: 2.115093115987804 msec\nrounds: 319"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 155241.08645154093,
            "unit": "iter/sec",
            "range": "stddev: 0.000001106908655043972",
            "extra": "mean: 6.441593671222815 usec\nrounds: 28125"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 95907.70168508022,
            "unit": "iter/sec",
            "range": "stddev: 0.000001769638012960784",
            "extra": "mean: 10.426691312899681 usec\nrounds: 12916"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 211.35208316927626,
            "unit": "iter/sec",
            "range": "stddev: 0.00029058225730497285",
            "extra": "mean: 4.73144141758508 msec\nrounds: 182"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18476.8803205858,
            "unit": "iter/sec",
            "range": "stddev: 0.000005618685802792364",
            "extra": "mean: 54.121690601949815 usec\nrounds: 8885"
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
          "id": "6ddfa3be83cc3f7578a6c9d3425e023c3138c4bc",
          "message": "Merge branch 'main' of https://github.com/iausathub/satchecker",
          "timestamp": "2025-09-05T13:58:47-07:00",
          "tree_id": "3bd19000044c5f90d649f83d9eb29e0c50c90912",
          "url": "https://github.com/iausathub/satchecker/commit/6ddfa3be83cc3f7578a6c9d3425e023c3138c4bc"
        },
        "date": 1757106210276,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 93054.17416806672,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019485572667711414",
            "extra": "mean: 10.74642818487522 usec\nrounds: 10729"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18489.150202862435,
            "unit": "iter/sec",
            "range": "stddev: 0.000006323732082066494",
            "extra": "mean: 54.08577403655811 usec\nrounds: 6563"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 223.65439698165758,
            "unit": "iter/sec",
            "range": "stddev: 0.00011915183946158335",
            "extra": "mean: 4.471184172972072 msec\nrounds: 185"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 144493.08499272162,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012331797998047544",
            "extra": "mean: 6.920746415306807 usec\nrounds: 15340"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1427.928768822399,
            "unit": "iter/sec",
            "range": "stddev: 0.00002020743490175904",
            "extra": "mean: 700.3150450037447 usec\nrounds: 911"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 101454.86282833992,
            "unit": "iter/sec",
            "range": "stddev: 0.0000026965655146094273",
            "extra": "mean: 9.856599990598625 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12490455.357666755,
            "unit": "iter/sec",
            "range": "stddev: 8.917073337264048e-9",
            "extra": "mean: 80.06113238989913 nsec\nrounds: 65799"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 740417.741142264,
            "unit": "iter/sec",
            "range": "stddev: 6.088721170800806e-7",
            "extra": "mean: 1.3505889235680264 usec\nrounds: 37105"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 200316.1024727067,
            "unit": "iter/sec",
            "range": "stddev: 7.964339248923284e-7",
            "extra": "mean: 4.992109908569388 usec\nrounds: 41780"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 485.95555458473075,
            "unit": "iter/sec",
            "range": "stddev: 0.00008154232882259573",
            "extra": "mean: 2.0578013576870045 msec\nrounds: 397"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 532.1695808644241,
            "unit": "iter/sec",
            "range": "stddev: 0.00004478000916271689",
            "extra": "mean: 1.8791002641971013 msec\nrounds: 405"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 163157.40794920898,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010024978290720728",
            "extra": "mean: 6.129050544314241 usec\nrounds: 30864"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 674351.9209733291,
            "unit": "iter/sec",
            "range": "stddev: 6.844139479247738e-7",
            "extra": "mean: 1.4829052441292747 usec\nrounds: 37908"
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
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "5fd2629b6749a586d36543a022d6ca744db7d7dc",
          "message": "Update quality_check.yml - fix incomplete permission",
          "timestamp": "2025-09-12T18:59:01Z",
          "url": "https://github.com/iausathub/satchecker/commit/5fd2629b6749a586d36543a022d6ca744db7d7dc"
        },
        "date": 1757707391733,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 481.33751259254024,
            "unit": "iter/sec",
            "range": "stddev: 0.00007443520446635101",
            "extra": "mean: 2.077544288235261 msec\nrounds: 340"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 504.7908300001646,
            "unit": "iter/sec",
            "range": "stddev: 0.00023888454979977648",
            "extra": "mean: 1.9810185537634943 msec\nrounds: 372"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 130439.10065133318,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011249618490000555",
            "extra": "mean: 7.666412870118017 usec\nrounds: 20808"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1403.8995325008827,
            "unit": "iter/sec",
            "range": "stddev: 0.00002042327973143672",
            "extra": "mean: 712.3016831686075 usec\nrounds: 909"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 745083.2920933935,
            "unit": "iter/sec",
            "range": "stddev: 4.090328226901422e-7",
            "extra": "mean: 1.3421318268866156 usec\nrounds: 53062"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 687238.8514208859,
            "unit": "iter/sec",
            "range": "stddev: 4.6378902283919207e-7",
            "extra": "mean: 1.4550981771948304 usec\nrounds: 49757"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12637707.153923703,
            "unit": "iter/sec",
            "range": "stddev: 8.878226932625902e-9",
            "extra": "mean: 79.12827760772738 nsec\nrounds: 121877"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 200305.95414284407,
            "unit": "iter/sec",
            "range": "stddev: 8.265569338491023e-7",
            "extra": "mean: 4.992362829548594 usec\nrounds: 44164"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 158413.55586341448,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013312353224758221",
            "extra": "mean: 6.312591081928674 usec\nrounds: 30769"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 142997.17055546836,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010861704396804558",
            "extra": "mean: 6.99314536165666 usec\nrounds: 22475"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 17860.14615085268,
            "unit": "iter/sec",
            "range": "stddev: 0.000005790338598301466",
            "extra": "mean: 55.9905832546761 usec\nrounds: 8492"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.33747273996701604,
            "unit": "iter/sec",
            "range": "stddev: 0.16386976755733873",
            "extra": "mean: 2.9632023021999885 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.12912762217580934,
            "unit": "iter/sec",
            "range": "stddev: 6.172550923761584",
            "extra": "mean: 7.744276423200017 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.214911262354919,
            "unit": "iter/sec",
            "range": "stddev: 0.19789285622086042",
            "extra": "mean: 4.6530832727999725 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.03771600976711009,
            "unit": "iter/sec",
            "range": "stddev: 1.1042915836705443",
            "extra": "mean: 26.513939469600018 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 6.780702624811874,
            "unit": "iter/sec",
            "range": "stddev: 0.031676663114348025",
            "extra": "mean: 147.47734200004743 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.05400201334479432,
            "unit": "iter/sec",
            "range": "stddev: 0.36673521557178784",
            "extra": "mean: 18.517828096799985 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.25646936499687345,
            "unit": "iter/sec",
            "range": "stddev: 0.14039056560653143",
            "extra": "mean: 3.8991011655999954 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.3192170038578864,
            "unit": "iter/sec",
            "range": "stddev: 0.1253547457599435",
            "extra": "mean: 3.1326652024000397 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.08755683763628841,
            "unit": "iter/sec",
            "range": "stddev: 7.618632171534511",
            "extra": "mean: 11.421152556400056 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.12768863591042548,
            "unit": "iter/sec",
            "range": "stddev: 0.13729427067700503",
            "extra": "mean: 7.831550496799946 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.1310856689192147,
            "unit": "iter/sec",
            "range": "stddev: 0.9871428626565611",
            "extra": "mean: 7.628598978399987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.9046077809878489,
            "unit": "iter/sec",
            "range": "stddev: 0.04889231378466678",
            "extra": "mean: 1.1054514685999948 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.1277590108262713,
            "unit": "iter/sec",
            "range": "stddev: 0.21905606044653766",
            "extra": "mean: 7.827236556800017 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.2743242136293144,
            "unit": "iter/sec",
            "range": "stddev: 0.08122439697941847",
            "extra": "mean: 3.6453216679999967 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.184069327247341,
            "unit": "iter/sec",
            "range": "stddev: 0.6165374097498915",
            "extra": "mean: 5.432735670600141 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.2661536084452704,
            "unit": "iter/sec",
            "range": "stddev: 0.0980535216286411",
            "extra": "mean: 3.7572287891998712 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.11948456158898756,
            "unit": "iter/sec",
            "range": "stddev: 1.027017978713543",
            "extra": "mean: 8.369282078800097 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.40714041664083567,
            "unit": "iter/sec",
            "range": "stddev: 0.06113273801196625",
            "extra": "mean: 2.4561550735999846 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.06188082840892623,
            "unit": "iter/sec",
            "range": "stddev: 2.929514306335057",
            "extra": "mean: 16.160093937199964 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.11598082279168705,
            "unit": "iter/sec",
            "range": "stddev: 0.06982590412048333",
            "extra": "mean: 8.622115069799928 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.9114892333167397,
            "unit": "iter/sec",
            "range": "stddev: 0.02580535124987424",
            "extra": "mean: 1.0971056634000889 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.3286517065349824,
            "unit": "iter/sec",
            "range": "stddev: 0.1026193821689342",
            "extra": "mean: 3.0427348469999744 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 6.198944255326052,
            "unit": "iter/sec",
            "range": "stddev: 0.004381888190378916",
            "extra": "mean: 161.31779199995435 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 223.30509297645133,
            "unit": "iter/sec",
            "range": "stddev: 0.00020327972221863573",
            "extra": "mean: 4.478178203062548 msec\nrounds: 197"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 95920.71447139911,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019813666747171284",
            "extra": "mean: 10.425276808151509 usec\nrounds: 13634"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 0.32240201811515873,
            "unit": "iter/sec",
            "range": "stddev: 6.552000545948021",
            "extra": "mean: 3.101717556999938 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.4607832672936913,
            "unit": "iter/sec",
            "range": "stddev: 0.10886316821883167",
            "extra": "mean: 406.37467480009946 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.439074235403115,
            "unit": "iter/sec",
            "range": "stddev: 0.11200491097536991",
            "extra": "mean: 409.9916211999698 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 3.659576894182008,
            "unit": "iter/sec",
            "range": "stddev: 0.05849666876735916",
            "extra": "mean: 273.25563280001006 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 6.158898762787122,
            "unit": "iter/sec",
            "range": "stddev: 0.006533699147746888",
            "extra": "mean: 162.3666890000095 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 5.875907317736253,
            "unit": "iter/sec",
            "range": "stddev: 0.013632356340144865",
            "extra": "mean: 170.18648285712905 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 5.5479037695538755,
            "unit": "iter/sec",
            "range": "stddev: 0.013053082374530863",
            "extra": "mean: 180.2482598000097 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.6823773425630858,
            "unit": "iter/sec",
            "range": "stddev: 0.03190468045599931",
            "extra": "mean: 1.4654648354001438 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 3.649460022247017,
            "unit": "iter/sec",
            "range": "stddev: 0.05793506191163371",
            "extra": "mean: 274.01313999989725 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.5291299292382337,
            "unit": "iter/sec",
            "range": "stddev: 0.10977186689946261",
            "extra": "mean: 395.3928931999144 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 4.418828355719939,
            "unit": "iter/sec",
            "range": "stddev: 0.15460253242291308",
            "extra": "mean: 226.30433216659185 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 4.11362690175195,
            "unit": "iter/sec",
            "range": "stddev: 0.051616370513956664",
            "extra": "mean: 243.0944818000171 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 6.222307290841994,
            "unit": "iter/sec",
            "range": "stddev: 0.007217849525725956",
            "extra": "mean: 160.712088500001 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.57076336626834,
            "unit": "iter/sec",
            "range": "stddev: 0.052038657267816445",
            "extra": "mean: 280.05216180008574 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.6755165537348534,
            "unit": "iter/sec",
            "range": "stddev: 0.01814370395320364",
            "extra": "mean: 1.4803486228000111 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 6.212478956777221,
            "unit": "iter/sec",
            "range": "stddev: 0.013641537079796531",
            "extra": "mean: 160.96634000008893 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.052188659450216855,
            "unit": "iter/sec",
            "range": "stddev: 32.005240177850084",
            "extra": "mean: 19.16125094100007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 5.626670595076621,
            "unit": "iter/sec",
            "range": "stddev: 0.013225613732858573",
            "extra": "mean: 177.72499439988678 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 5.42665683891955,
            "unit": "iter/sec",
            "range": "stddev: 0.011832417011143695",
            "extra": "mean: 184.2755179999737 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.6606069578857333,
            "unit": "iter/sec",
            "range": "stddev: 0.2521745519951132",
            "extra": "mean: 1.513759411799856 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.0891758959204298,
            "unit": "iter/sec",
            "range": "stddev: 0.10835939732178239",
            "extra": "mean: 918.1253493999975 msec\nrounds: 5"
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
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "5fd2629b6749a586d36543a022d6ca744db7d7dc",
          "message": "Update quality_check.yml - fix incomplete permission",
          "timestamp": "2025-09-12T18:59:01Z",
          "url": "https://github.com/iausathub/satchecker/commit/5fd2629b6749a586d36543a022d6ca744db7d7dc"
        },
        "date": 1758065669384,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 110982.62942702416,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053814477480239615",
            "extra": "mean: 9.010419064341443 usec\nrounds: 12578"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 477.19539197798105,
            "unit": "iter/sec",
            "range": "stddev: 0.00026231860330765036",
            "extra": "mean: 2.0955776539563535 msec\nrounds: 367"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 202585.53037865667,
            "unit": "iter/sec",
            "range": "stddev: 7.96662978762144e-7",
            "extra": "mean: 4.936186696704746 usec\nrounds: 49535"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1401.2747152705363,
            "unit": "iter/sec",
            "range": "stddev: 0.00002132372476121335",
            "extra": "mean: 713.6359409774518 usec\nrounds: 881"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 129343.58146988074,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012007627237576796",
            "extra": "mean: 7.7313461451727505 usec\nrounds: 20321"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 157616.00779815667,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010116189417820405",
            "extra": "mean: 6.344533235993401 usec\nrounds: 38287"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 523.3984674450926,
            "unit": "iter/sec",
            "range": "stddev: 0.00006523136775253127",
            "extra": "mean: 1.910590233252652 msec\nrounds: 403"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 679811.5452582535,
            "unit": "iter/sec",
            "range": "stddev: 4.710731587038737e-7",
            "extra": "mean: 1.4709959061082292 usec\nrounds: 17344"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11800635.267939763,
            "unit": "iter/sec",
            "range": "stddev: 1.4863139548353994e-8",
            "extra": "mean: 84.74120056204288 nsec\nrounds: 194970"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 741767.1001895622,
            "unit": "iter/sec",
            "range": "stddev: 4.677954453804641e-7",
            "extra": "mean: 1.348132048111119 usec\nrounds: 34586"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 96064.65196528466,
            "unit": "iter/sec",
            "range": "stddev: 0.0000017357604394958",
            "extra": "mean: 10.40965620071548 usec\nrounds: 12900"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18107.57663432586,
            "unit": "iter/sec",
            "range": "stddev: 0.000005257033828021978",
            "extra": "mean: 55.22550146795111 usec\nrounds: 8495"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 224.09046247341294,
            "unit": "iter/sec",
            "range": "stddev: 0.00009099838611927208",
            "extra": "mean: 4.462483538846033 msec\nrounds: 193"
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
          "id": "d05b8b73489aac4f8de1880ca4b941ffef6176cc",
          "message": "Create update_wiki.yml to enable manual trigger",
          "timestamp": "2025-09-30T18:57:59-07:00",
          "tree_id": "4d9fcedce0f3d3d11f8cc190884f67817508ccd1",
          "url": "https://github.com/iausathub/satchecker/commit/d05b8b73489aac4f8de1880ca4b941ffef6176cc"
        },
        "date": 1759286463874,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1417.843393517806,
            "unit": "iter/sec",
            "range": "stddev: 0.00003786617474191851",
            "extra": "mean: 705.2965119926988 usec\nrounds: 834"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 663398.6537715179,
            "unit": "iter/sec",
            "range": "stddev: 6.072119382032898e-7",
            "extra": "mean: 1.5073892512667222 usec\nrounds: 54425"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 502.8722048855591,
            "unit": "iter/sec",
            "range": "stddev: 0.00013150438316353576",
            "extra": "mean: 1.988576799999464 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133712.7410549865,
            "unit": "iter/sec",
            "range": "stddev: 0.000001136031981250355",
            "extra": "mean: 7.478718872338213 usec\nrounds: 26632"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 202845.13223160224,
            "unit": "iter/sec",
            "range": "stddev: 9.192973864018479e-7",
            "extra": "mean: 4.929869349086628 usec\nrounds: 51718"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 482.37694927828875,
            "unit": "iter/sec",
            "range": "stddev: 0.00018547545003763338",
            "extra": "mean: 2.0730675491359114 msec\nrounds: 346"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 161569.9493861585,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010578695532853295",
            "extra": "mean: 6.189269748484979 usec\nrounds: 34610"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 144700.91434362222,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011169742240712977",
            "extra": "mean: 6.910806365917588 usec\nrounds: 21489"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 726293.9846935007,
            "unit": "iter/sec",
            "range": "stddev: 4.618172478498785e-7",
            "extra": "mean: 1.3768529288067897 usec\nrounds: 72543"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12206526.619873168,
            "unit": "iter/sec",
            "range": "stddev: 8.77662690974352e-9",
            "extra": "mean: 81.92338665545361 nsec\nrounds: 103019"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 225.83539964892086,
            "unit": "iter/sec",
            "range": "stddev: 0.00009757729975468265",
            "extra": "mean: 4.428003765373275 msec\nrounds: 179"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.112931108425356,
            "unit": "iter/sec",
            "range": "stddev: 7.797175898671847",
            "extra": "mean: 8.854956034199995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.19533481800252017,
            "unit": "iter/sec",
            "range": "stddev: 0.0992334781076366",
            "extra": "mean: 5.119415013800039 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.05898686559151349,
            "unit": "iter/sec",
            "range": "stddev: 1.2301631323061875",
            "extra": "mean: 16.952926553599944 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.24070975336647416,
            "unit": "iter/sec",
            "range": "stddev: 0.022931514663639043",
            "extra": "mean: 4.154380892400013 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.22562638513690667,
            "unit": "iter/sec",
            "range": "stddev: 0.1792742808829113",
            "extra": "mean: 4.432105754799977 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.1067583876816488,
            "unit": "iter/sec",
            "range": "stddev: 1.1816274047173667",
            "extra": "mean: 9.36694550860002 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.11885352889465217,
            "unit": "iter/sec",
            "range": "stddev: 6.162091995019606",
            "extra": "mean: 8.413717365399952 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.12602970324129237,
            "unit": "iter/sec",
            "range": "stddev: 0.11596460854985748",
            "extra": "mean: 7.934637424999982 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18750.469061623473,
            "unit": "iter/sec",
            "range": "stddev: 0.000004881133376638109",
            "extra": "mean: 53.331999146981175 usec\nrounds: 9394"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.11981499227769542,
            "unit": "iter/sec",
            "range": "stddev: 0.13277564539837983",
            "extra": "mean: 8.346200930199938 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.3737158719493882,
            "unit": "iter/sec",
            "range": "stddev: 0.11353398824374987",
            "extra": "mean: 2.675829620999957 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.3779171542003562,
            "unit": "iter/sec",
            "range": "stddev: 0.09012674893284976",
            "extra": "mean: 2.6460825842000304 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.0647429795599237,
            "unit": "iter/sec",
            "range": "stddev: 0.10673142634705549",
            "extra": "mean: 15.445690124200064 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.24632583495673566,
            "unit": "iter/sec",
            "range": "stddev: 0.13482270097390184",
            "extra": "mean: 4.059663494800043 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.1311546657591465,
            "unit": "iter/sec",
            "range": "stddev: 0.14300489263314892",
            "extra": "mean: 7.624585783600014 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.1312561396316105,
            "unit": "iter/sec",
            "range": "stddev: 0.10935202447635542",
            "extra": "mean: 7.6186912307999135 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.14031946926855826,
            "unit": "iter/sec",
            "range": "stddev: 0.16221710107472814",
            "extra": "mean: 7.126594799799977 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 96928.04381794015,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018590724698330686",
            "extra": "mean: 10.31693161865826 usec\nrounds: 13717"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.2297630673429497,
            "unit": "iter/sec",
            "range": "stddev: 0.13954044345875863",
            "extra": "mean: 4.352309583799979 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.19685832191393987,
            "unit": "iter/sec",
            "range": "stddev: 0.13956692128510043",
            "extra": "mean: 5.079795409600047 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 10.186263648758139,
            "unit": "iter/sec",
            "range": "stddev: 0.0038727204451377297",
            "extra": "mean: 98.17142325016448 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.2376596429735329,
            "unit": "iter/sec",
            "range": "stddev: 0.028112656690898668",
            "extra": "mean: 4.207697981400088 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.14107395315159116,
            "unit": "iter/sec",
            "range": "stddev: 0.16449438495600413",
            "extra": "mean: 7.088480741199964 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.13008649908812756,
            "unit": "iter/sec",
            "range": "stddev: 0.3984456943088544",
            "extra": "mean: 7.6871928063998896 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.13338107217969647,
            "unit": "iter/sec",
            "range": "stddev: 0.08021951754301025",
            "extra": "mean: 7.497315651000008 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.05150557027319474,
            "unit": "iter/sec",
            "range": "stddev: 0.20060409270234209",
            "extra": "mean: 19.415375748600034 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 7.9313568900218305,
            "unit": "iter/sec",
            "range": "stddev: 0.005126020650601617",
            "extra": "mean: 126.08183112502047 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.3186753156003923,
            "unit": "iter/sec",
            "range": "stddev: 0.06899154853432284",
            "extra": "mean: 3.1379901455999972 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.9116244234216091,
            "unit": "iter/sec",
            "range": "stddev: 0.04055907983760209",
            "extra": "mean: 1.0969429671999023 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.05972043542445132,
            "unit": "iter/sec",
            "range": "stddev: 0.15709677456075186",
            "extra": "mean: 16.744687022000015 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.357509478669902,
            "unit": "iter/sec",
            "range": "stddev: 0.04629189837078166",
            "extra": "mean: 2.797128634799992 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.26097771880933823,
            "unit": "iter/sec",
            "range": "stddev: 0.07908247086168413",
            "extra": "mean: 3.8317447350000293 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.13444640599336802,
            "unit": "iter/sec",
            "range": "stddev: 0.1207782134759142",
            "extra": "mean: 7.43790800959996 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.13389841832608873,
            "unit": "iter/sec",
            "range": "stddev: 0.216287237050529",
            "extra": "mean: 7.4683481141999435 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.8343470388426785,
            "unit": "iter/sec",
            "range": "stddev: 0.03595467000153185",
            "extra": "mean: 1.1985420375999638 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.33911526683201393,
            "unit": "iter/sec",
            "range": "stddev: 0.08497027075657991",
            "extra": "mean: 2.948849838999922 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.03489616772869222,
            "unit": "iter/sec",
            "range": "stddev: 0.08976243043072121",
            "extra": "mean: 28.656441812600043 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.778929427082158,
            "unit": "iter/sec",
            "range": "stddev: 0.04561575105250715",
            "extra": "mean: 1.2838133535999077 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.464417062056884,
            "unit": "iter/sec",
            "range": "stddev: 0.0316488467227758",
            "extra": "mean: 682.8655756000444 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 7.708509530813995,
            "unit": "iter/sec",
            "range": "stddev: 0.009603201409961598",
            "extra": "mean: 129.72676442866162 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.5879470447093668,
            "unit": "iter/sec",
            "range": "stddev: 0.04961011428154331",
            "extra": "mean: 1.7008334492000359 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 1.9306205041442797,
            "unit": "iter/sec",
            "range": "stddev: 0.14892778056093944",
            "extra": "mean: 517.9681858000549 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 6.855576529489544,
            "unit": "iter/sec",
            "range": "stddev: 0.0258831177141954",
            "extra": "mean: 145.86665260003429 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 8.6885169035957,
            "unit": "iter/sec",
            "range": "stddev: 0.00774956167122249",
            "extra": "mean: 115.09444144444893 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 3.9713178336590675,
            "unit": "iter/sec",
            "range": "stddev: 0.05865236736093321",
            "extra": "mean: 251.805582399993 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 8.944034496292055,
            "unit": "iter/sec",
            "range": "stddev: 0.005973877200466454",
            "extra": "mean: 111.80636662510324 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 9.0383302843374,
            "unit": "iter/sec",
            "range": "stddev: 0.00309078342475531",
            "extra": "mean: 110.63990455548061 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.6225430865513,
            "unit": "iter/sec",
            "range": "stddev: 0.02200060060413976",
            "extra": "mean: 1.6063145211999654 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.381343375988541,
            "unit": "iter/sec",
            "range": "stddev: 0.15039823092265256",
            "extra": "mean: 419.93103980012165 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 8.450999075943848,
            "unit": "iter/sec",
            "range": "stddev: 0.006618017522393752",
            "extra": "mean: 118.32920475006858 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.6195257607222125,
            "unit": "iter/sec",
            "range": "stddev: 0.01054567312722502",
            "extra": "mean: 1.6141378831999647 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 8.253009636116532,
            "unit": "iter/sec",
            "range": "stddev: 0.006967431768025791",
            "extra": "mean: 121.16791862496257 msec\nrounds: 8"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 8.974193405611107,
            "unit": "iter/sec",
            "range": "stddev: 0.002642787769787847",
            "extra": "mean: 111.43062722213573 msec\nrounds: 9"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 6.91765448919995,
            "unit": "iter/sec",
            "range": "stddev: 0.013367965622374784",
            "extra": "mean: 144.55766785710824 msec\nrounds: 7"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 7.12267337740858,
            "unit": "iter/sec",
            "range": "stddev: 0.015272604802814288",
            "extra": "mean: 140.39672283327795 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.2396518538951415,
            "unit": "iter/sec",
            "range": "stddev: 0.13999849675196213",
            "extra": "mean: 446.49796720004815 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 3.623512765326402,
            "unit": "iter/sec",
            "range": "stddev: 0.06579392302226374",
            "extra": "mean: 275.9752938002748 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.1849546350954028,
            "unit": "iter/sec",
            "range": "stddev: 0.09090596744791635",
            "extra": "mean: 313.97621460000664 msec\nrounds: 5"
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
            "name": "GitHub",
            "username": "web-flow",
            "email": "noreply@github.com"
          },
          "id": "d05b8b73489aac4f8de1880ca4b941ffef6176cc",
          "message": "Create update_wiki.yml to enable manual trigger",
          "timestamp": "2025-10-01T01:57:59Z",
          "url": "https://github.com/iausathub/satchecker/commit/d05b8b73489aac4f8de1880ca4b941ffef6176cc"
        },
        "date": 1761335201393,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 0.17557276818420056,
            "unit": "iter/sec",
            "range": "stddev: 7.365378671893769",
            "extra": "mean: 5.6956440929999985 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 1.7672413191479353,
            "unit": "iter/sec",
            "range": "stddev: 0.13276412194552684",
            "extra": "mean: 565.8536778000098 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 4.293169846174308,
            "unit": "iter/sec",
            "range": "stddev: 0.009779626097558496",
            "extra": "mean: 232.9281243999958 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 4.546057443592966,
            "unit": "iter/sec",
            "range": "stddev: 0.01068281570717414",
            "extra": "mean: 219.97082359998785 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.6521487488632597,
            "unit": "iter/sec",
            "range": "stddev: 0.05997771374513339",
            "extra": "mean: 1.5333924993999744 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 1.9317883299809602,
            "unit": "iter/sec",
            "range": "stddev: 0.12880187278606",
            "extra": "mean: 517.6550579999912 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 3.6847706967932545,
            "unit": "iter/sec",
            "range": "stddev: 0.01161519218241838",
            "extra": "mean: 271.3873079999985 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.4741794104997537,
            "unit": "iter/sec",
            "range": "stddev: 0.9166014057110711",
            "extra": "mean: 2.1089064136000046 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 1.9186564367932213,
            "unit": "iter/sec",
            "range": "stddev: 0.12562489913907762",
            "extra": "mean: 521.1980533999963 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 4.396474209522238,
            "unit": "iter/sec",
            "range": "stddev: 0.006814590948913054",
            "extra": "mean: 227.45499059999474 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 2.911443874083942,
            "unit": "iter/sec",
            "range": "stddev: 0.05162599182276954",
            "extra": "mean: 343.47218880001265 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 3.960637571047572,
            "unit": "iter/sec",
            "range": "stddev: 0.010996985657229242",
            "extra": "mean: 252.48460179998344 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 4.367621762907112,
            "unit": "iter/sec",
            "range": "stddev: 0.007020962579654649",
            "extra": "mean: 228.9575549999995 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.6634907717488338,
            "unit": "iter/sec",
            "range": "stddev: 0.023087426359172356",
            "extra": "mean: 1.5071799677999933 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 2.82454434378621,
            "unit": "iter/sec",
            "range": "stddev: 0.04738862690072905",
            "extra": "mean: 354.03940539999894 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 4.429448203040708,
            "unit": "iter/sec",
            "range": "stddev: 0.0025940697411357154",
            "extra": "mean: 225.761754999985 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 4.448029647277633,
            "unit": "iter/sec",
            "range": "stddev: 0.009377783594606682",
            "extra": "mean: 224.8186454000006 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 2.644716649707484,
            "unit": "iter/sec",
            "range": "stddev: 0.059939924376673316",
            "extra": "mean: 378.1123396000112 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.0060121501330708,
            "unit": "iter/sec",
            "range": "stddev: 0.03657986042113825",
            "extra": "mean: 994.0237797999998 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 3.079648755588433,
            "unit": "iter/sec",
            "range": "stddev: 0.008766637357709002",
            "extra": "mean: 324.71235500001967 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.6020842173301827,
            "unit": "iter/sec",
            "range": "stddev: 0.08800213398545174",
            "extra": "mean: 1.6608972154000186 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 147192.76469061157,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010450511629416377",
            "extra": "mean: 6.793812196556853 usec\nrounds: 12774"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 119823.61967456818,
            "unit": "iter/sec",
            "range": "stddev: 0.0000027856019609930754",
            "extra": "mean: 8.34559999702833 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 486.00290150048596,
            "unit": "iter/sec",
            "range": "stddev: 0.00009812704303633558",
            "extra": "mean: 2.0576008845062423 msec\nrounds: 355"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 203632.44729307908,
            "unit": "iter/sec",
            "range": "stddev: 8.053535537726618e-7",
            "extra": "mean: 4.91080873059854 usec\nrounds: 54933"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133750.38835629137,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010690233113720239",
            "extra": "mean: 7.4766138049345106 usec\nrounds: 18703"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 538.1660952416713,
            "unit": "iter/sec",
            "range": "stddev: 0.00004821483338420204",
            "extra": "mean: 1.858162394178577 msec\nrounds: 378"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12593379.959738875,
            "unit": "iter/sec",
            "range": "stddev: 8.486089267021794e-9",
            "extra": "mean: 79.40679969931116 nsec\nrounds: 122026"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 718485.1303476974,
            "unit": "iter/sec",
            "range": "stddev: 4.5870588555808434e-7",
            "extra": "mean: 1.391817252384985 usec\nrounds: 33642"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1433.186636558724,
            "unit": "iter/sec",
            "range": "stddev: 0.00005202583295779493",
            "extra": "mean: 697.7458305089531 usec\nrounds: 826"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 675163.9443689525,
            "unit": "iter/sec",
            "range": "stddev: 4.627378325795806e-7",
            "extra": "mean: 1.4811217458222805 usec\nrounds: 62228"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1980]",
            "value": 0.7914022436326141,
            "unit": "iter/sec",
            "range": "stddev: 0.014293814755420626",
            "extra": "mean: 1.2635799405999932 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2019]",
            "value": 0.1921975714746157,
            "unit": "iter/sec",
            "range": "stddev: 0.1265937652600421",
            "extra": "mean: 5.202979373400012 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1980_radius1_duration30]",
            "value": 0.8873240022278692,
            "unit": "iter/sec",
            "range": "stddev: 0.09925870483286567",
            "extra": "mean: 1.1269840525999826 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2015]",
            "value": 0.22108279053569002,
            "unit": "iter/sec",
            "range": "stddev: 0.21154427552368235",
            "extra": "mean: 4.523192409399985 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_240_radius1_duration240]",
            "value": 0.0734081898790333,
            "unit": "iter/sec",
            "range": "stddev: 0.14313700491357711",
            "extra": "mean: 13.622458225000013 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2019_radius1_duration30]",
            "value": 0.24251984199393486,
            "unit": "iter/sec",
            "range": "stddev: 0.06670081912893541",
            "extra": "mean: 4.12337395479999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_1960]",
            "value": 4.724406704942823,
            "unit": "iter/sec",
            "range": "stddev: 0.008905332018114782",
            "extra": "mean: 211.6667896000081 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2000]",
            "value": 0.3536034956363502,
            "unit": "iter/sec",
            "range": "stddev: 0.05891686026023964",
            "extra": "mean: 2.828026341200007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2020_radius1_duration30]",
            "value": 0.2202776132246861,
            "unit": "iter/sec",
            "range": "stddev: 0.12429573045573089",
            "extra": "mean: 4.5397259637999925 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_60_radius1_duration60]",
            "value": 0.1091739254456213,
            "unit": "iter/sec",
            "range": "stddev: 0.20107721115447008",
            "extra": "mean: 9.159696291199975 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2023_radius1_duration30]",
            "value": 0.2900186546361623,
            "unit": "iter/sec",
            "range": "stddev: 0.15012468959301856",
            "extra": "mean: 3.4480540614000574 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_1_radius1_duration30]",
            "value": 0.1590829167651731,
            "unit": "iter/sec",
            "range": "stddev: 0.15749150721543465",
            "extra": "mean: 6.286030079999909 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_1960_radius1_duration30]",
            "value": 3.871464875991038,
            "unit": "iter/sec",
            "range": "stddev: 0.019187887087474573",
            "extra": "mean: 258.3001607999904 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2021]",
            "value": 0.29772355624304325,
            "unit": "iter/sec",
            "range": "stddev: 0.154089612316341",
            "extra": "mean: 3.358820553599935 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2022_radius1_duration30]",
            "value": 0.36711417359698967,
            "unit": "iter/sec",
            "range": "stddev: 0.01427451569615645",
            "extra": "mean: 2.723948220800048 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_2_radius2_duration30]",
            "value": 0.1579048108565522,
            "unit": "iter/sec",
            "range": "stddev: 0.12121610987729876",
            "extra": "mean: 6.332929279200016 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.1517719553757921,
            "unit": "iter/sec",
            "range": "stddev: 0.12097310668076885",
            "extra": "mean: 6.58883255159999 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_300_radius1_duration300]",
            "value": 0.06730859137068138,
            "unit": "iter/sec",
            "range": "stddev: 0.07630983736305381",
            "extra": "mean: 14.856944405400009 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2020]",
            "value": 0.1712904085674029,
            "unit": "iter/sec",
            "range": "stddev: 0.19147986332980788",
            "extra": "mean: 5.838038500599987 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2024_radius1_duration30]",
            "value": 0.1716754037302851,
            "unit": "iter/sec",
            "range": "stddev: 0.08567135767988401",
            "extra": "mean: 5.824946254799988 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2025]",
            "value": 0.12656254762975822,
            "unit": "iter/sec",
            "range": "stddev: 0.3724138617029384",
            "extra": "mean: 7.901231594399997 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 207.73825763131265,
            "unit": "iter/sec",
            "range": "stddev: 0.006014046179908585",
            "extra": "mean: 4.813749818652897 msec\nrounds: 193"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2010]",
            "value": 0.22702002140121738,
            "unit": "iter/sec",
            "range": "stddev: 0.21217293155986866",
            "extra": "mean: 4.404897831599965 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2023]",
            "value": 0.23328974414778555,
            "unit": "iter/sec",
            "range": "stddev: 0.08226836355573838",
            "extra": "mean: 4.286515052999993 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2000_radius1_duration30]",
            "value": 0.45419011304733226,
            "unit": "iter/sec",
            "range": "stddev: 0.05586486040405367",
            "extra": "mean: 2.2017211983999916 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_180_radius1_duration180]",
            "value": 0.08077128251221562,
            "unit": "iter/sec",
            "range": "stddev: 0.05010007031836091",
            "extra": "mean: 12.380637881400025 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2021_radius1_duration30]",
            "value": 0.39296280835290237,
            "unit": "iter/sec",
            "range": "stddev: 0.06717229666882724",
            "extra": "mean: 2.544770087000052 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_30_radius1_duration30]",
            "value": 0.15858976252112955,
            "unit": "iter/sec",
            "range": "stddev: 0.17234289502643982",
            "extra": "mean: 6.305577258599942 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.2861478856872276,
            "unit": "iter/sec",
            "range": "stddev: 0.08058632387418498",
            "extra": "mean: 3.4946964489999575 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2015_radius1_duration30]",
            "value": 0.2789949608266676,
            "unit": "iter/sec",
            "range": "stddev: 0.09691620478133195",
            "extra": "mean: 3.5842941285999586 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_20_radius20_duration30]",
            "value": 0.13611330932343768,
            "unit": "iter/sec",
            "range": "stddev: 0.09950193246895385",
            "extra": "mean: 7.3468201233999935 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_duration_600_radius1_duration600]",
            "value": 0.04653316127972825,
            "unit": "iter/sec",
            "range": "stddev: 0.16751345900119832",
            "extra": "mean: 21.49005080459988 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2022]",
            "value": 0.27922639067255084,
            "unit": "iter/sec",
            "range": "stddev: 0.1539422556739853",
            "extra": "mean: 3.5813233755999136 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2025_radius1_duration30]",
            "value": 0.15924867468485615,
            "unit": "iter/sec",
            "range": "stddev: 0.07535627354862592",
            "extra": "mean: 6.27948711020008 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 96248.90173824411,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016755948363933155",
            "extra": "mean: 10.389728941734553 usec\nrounds: 13440"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_45_radius45_duration30]",
            "value": 0.06234755285210577,
            "unit": "iter/sec",
            "range": "stddev: 0.7195577624404511",
            "extra": "mean: 16.03912189419998 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.09677939509496433,
            "unit": "iter/sec",
            "range": "stddev: 7.098495413547227",
            "extra": "mean: 10.33277795360009 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_5_radius5_duration30]",
            "value": 0.15360470352957775,
            "unit": "iter/sec",
            "range": "stddev: 0.12156555433866498",
            "extra": "mean: 6.510217311199995 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18563.42045969362,
            "unit": "iter/sec",
            "range": "stddev: 0.0000053052046126804155",
            "extra": "mean: 53.869382648056686 usec\nrounds: 9084"
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
          "id": "a11796dfba926dc4bac721e20d86f45aa96c15e9",
          "message": "Add fix from develop to address failure to retrieve Starlink generation data from wikipedia",
          "timestamp": "2025-11-27T13:03:28-08:00",
          "tree_id": "8887e31a1ca1fed7a0481e0f92ce86373ea74960",
          "url": "https://github.com/iausathub/satchecker/commit/a11796dfba926dc4bac721e20d86f45aa96c15e9"
        },
        "date": 1764277589922,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 105869.39957320159,
            "unit": "iter/sec",
            "range": "stddev: 0.000004547500366997119",
            "extra": "mean: 9.445599994251097 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 741751.512814608,
            "unit": "iter/sec",
            "range": "stddev: 4.782351746804629e-7",
            "extra": "mean: 1.3481603781372242 usec\nrounds: 50437"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 491.0013169849002,
            "unit": "iter/sec",
            "range": "stddev: 0.00009173903234183297",
            "extra": "mean: 2.0366544149834795 msec\nrounds: 347"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1414.3648024236443,
            "unit": "iter/sec",
            "range": "stddev: 0.000014510526729328726",
            "extra": "mean: 707.0311692474303 usec\nrounds: 904"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 131444.63455315583,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010743719055829375",
            "extra": "mean: 7.607765835398955 usec\nrounds: 26144"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 684159.6773469952,
            "unit": "iter/sec",
            "range": "stddev: 4.481809139574357e-7",
            "extra": "mean: 1.4616470878227679 usec\nrounds: 48641"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 11626720.112902831,
            "unit": "iter/sec",
            "range": "stddev: 3.005811678899887e-8",
            "extra": "mean: 86.00877894105103 nsec\nrounds: 64313"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 142186.1310427158,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010640743312175327",
            "extra": "mean: 7.033034745840142 usec\nrounds: 16002"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 198568.17597995978,
            "unit": "iter/sec",
            "range": "stddev: 7.798115159440439e-7",
            "extra": "mean: 5.036053713365044 usec\nrounds: 40232"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 532.0194430705402,
            "unit": "iter/sec",
            "range": "stddev: 0.00011850359187173987",
            "extra": "mean: 1.8796305530273834 msec\nrounds: 396"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 225.98819090464505,
            "unit": "iter/sec",
            "range": "stddev: 0.00010113326913554779",
            "extra": "mean: 4.42500997949024 msec\nrounds: 195"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 19063.571295874634,
            "unit": "iter/sec",
            "range": "stddev: 0.000005253417696927632",
            "extra": "mean: 52.45606840814767 usec\nrounds: 7119"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 96877.51179475075,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016183923913193395",
            "extra": "mean: 10.322313006125167 usec\nrounds: 13463"
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
          "id": "45d8b0d5afb6b46300d8ce1fbbcddad4de60ae3c",
          "message": "updates to address mypy typing errors",
          "timestamp": "2025-11-29T19:55:19-08:00",
          "tree_id": "d6413d0a5729954778eb50326c8653f409c0f59e",
          "url": "https://github.com/iausathub/satchecker/commit/45d8b0d5afb6b46300d8ce1fbbcddad4de60ae3c"
        },
        "date": 1764475103831,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18087.996626556273,
            "unit": "iter/sec",
            "range": "stddev: 0.000006415829849293006",
            "extra": "mean: 55.285282314340385 usec\nrounds: 7690"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 98273.59341833736,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019546752761115337",
            "extra": "mean: 10.17567349698037 usec\nrounds: 11859"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 217.88961027594894,
            "unit": "iter/sec",
            "range": "stddev: 0.00020643840769321115",
            "extra": "mean: 4.589479960671543 msec\nrounds: 178"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 117365.38172908871,
            "unit": "iter/sec",
            "range": "stddev: 0.0000028037022588205207",
            "extra": "mean: 8.520400012912432 usec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 521.1033892611505,
            "unit": "iter/sec",
            "range": "stddev: 0.00003217479559528191",
            "extra": "mean: 1.9190049817520012 msec\nrounds: 274"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 199887.04803642217,
            "unit": "iter/sec",
            "range": "stddev: 0.0000019507932675896826",
            "extra": "mean: 5.002825394758875 usec\nrounds: 61997"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1385.197943201651,
            "unit": "iter/sec",
            "range": "stddev: 0.00002170744256781876",
            "extra": "mean: 721.9184845803834 usec\nrounds: 908"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 483.8708112521513,
            "unit": "iter/sec",
            "range": "stddev: 0.00009305657266511128",
            "extra": "mean: 2.0666673350521387 msec\nrounds: 388"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12150368.477690583,
            "unit": "iter/sec",
            "range": "stddev: 8.55770330299853e-9",
            "extra": "mean: 82.30203074387825 nsec\nrounds: 122625"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 141785.017527037,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011427822226751208",
            "extra": "mean: 7.052931384723423 usec\nrounds: 18713"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 684600.3825453125,
            "unit": "iter/sec",
            "range": "stddev: 5.120139291097052e-7",
            "extra": "mean: 1.4607061659563296 usec\nrounds: 37967"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 739812.0198247919,
            "unit": "iter/sec",
            "range": "stddev: 5.217386957571101e-7",
            "extra": "mean: 1.3516947186622188 usec\nrounds: 49266"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 130848.77839967777,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011481680631169633",
            "extra": "mean: 7.642409904244567 usec\nrounds: 20900"
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
          "id": "21c5b199a6504a36e5df68436789790586edad0c",
          "message": "Redis and Celery deployment changes for production",
          "timestamp": "2026-01-15T09:33:44-08:00",
          "tree_id": "56de9e9b8160f306c88a4b81b135a8e0819e810e",
          "url": "https://github.com/iausathub/satchecker/commit/21c5b199a6504a36e5df68436789790586edad0c"
        },
        "date": 1768498616810,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 528.002571947077,
            "unit": "iter/sec",
            "range": "stddev: 0.00003441776176296617",
            "extra": "mean: 1.8939301683936351 msec\nrounds: 386"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 142034.75165607093,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010435266652997939",
            "extra": "mean: 7.04053049229419 usec\nrounds: 28204"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 159176.90535475264,
            "unit": "iter/sec",
            "range": "stddev: 8.887065586727659e-7",
            "extra": "mean: 6.282318391423247 usec\nrounds: 34043"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 748901.2715654306,
            "unit": "iter/sec",
            "range": "stddev: 4.384106387105543e-7",
            "extra": "mean: 1.3352894940473221 usec\nrounds: 56806"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 197914.84092560763,
            "unit": "iter/sec",
            "range": "stddev: 8.90462119494007e-7",
            "extra": "mean: 5.052678188877613 usec\nrounds: 40328"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12162948.237870838,
            "unit": "iter/sec",
            "range": "stddev: 9.339891639057973e-9",
            "extra": "mean: 82.21690830570013 nsec\nrounds: 28748"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 128023.9721057365,
            "unit": "iter/sec",
            "range": "stddev: 0.0000012854309068756892",
            "extra": "mean: 7.811037132749548 usec\nrounds: 15889"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1391.0695141033707,
            "unit": "iter/sec",
            "range": "stddev: 0.0000192112806996053",
            "extra": "mean: 718.8713359479818 usec\nrounds: 765"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 694957.0275690258,
            "unit": "iter/sec",
            "range": "stddev: 4.39561442267491e-7",
            "extra": "mean: 1.4389378915960043 usec\nrounds: 79152"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 462.2934269393598,
            "unit": "iter/sec",
            "range": "stddev: 0.00029630378479942053",
            "extra": "mean: 2.1631283114288635 msec\nrounds: 350"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 95265.91315680984,
            "unit": "iter/sec",
            "range": "stddev: 0.0000016268289574197609",
            "extra": "mean: 10.496933970012732 usec\nrounds: 13191"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 214.1967065353368,
            "unit": "iter/sec",
            "range": "stddev: 0.00032044141154926405",
            "extra": "mean: 4.668605863157968 msec\nrounds: 190"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18502.27342151212,
            "unit": "iter/sec",
            "range": "stddev: 0.000005762223255821971",
            "extra": "mean: 54.047412294606225 usec\nrounds: 8996"
          }
        ]
      }
    ]
  }
}