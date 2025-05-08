window.BENCHMARK_DATA = {
  "lastUpdate": 1746745074737,
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
      }
    ]
  }
}