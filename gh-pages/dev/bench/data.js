window.BENCHMARK_DATA = {
  "lastUpdate": 1757101559296,
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
          "id": "4a0ab5d730dc31ebce909d8f897733fef070e0c5",
          "message": "Add missing token to benchmark workflow step",
          "timestamp": "2025-09-05T12:33:45-07:00",
          "tree_id": "feebe126ca19285562b6e003e7033186a1a355f8",
          "url": "https://github.com/iausathub/satchecker/commit/4a0ab5d730dc31ebce909d8f897733fef070e0c5"
        },
        "date": 1757101545483,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 475.70788186970117,
            "unit": "iter/sec",
            "range": "stddev: 0.0001887001688936812",
            "extra": "mean: 2.1021304000043983 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1415.4963398241262,
            "unit": "iter/sec",
            "range": "stddev: 0.000016103061277338396",
            "extra": "mean: 706.4659737122661 usec\nrounds: 951"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 196807.9734075357,
            "unit": "iter/sec",
            "range": "stddev: 7.926244529974474e-7",
            "extra": "mean: 5.0810949510123375 usec\nrounds: 36166"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 127906.05166228433,
            "unit": "iter/sec",
            "range": "stddev: 0.000001084860231834783",
            "extra": "mean: 7.8182383632663575 usec\nrounds: 17595"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 656760.4971634501,
            "unit": "iter/sec",
            "range": "stddev: 4.7166048529140786e-7",
            "extra": "mean: 1.5226250730959032 usec\nrounds: 47916"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 156945.79551771635,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011774343456902814",
            "extra": "mean: 6.371626565090863 usec\nrounds: 30589"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 485.5065366368969,
            "unit": "iter/sec",
            "range": "stddev: 0.00008632312388685655",
            "extra": "mean: 2.0597045035212065 msec\nrounds: 284"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 707443.5340405798,
            "unit": "iter/sec",
            "range": "stddev: 4.989502477759699e-7",
            "extra": "mean: 1.4135403772630124 usec\nrounds: 58783"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 138309.08724782043,
            "unit": "iter/sec",
            "range": "stddev: 0.0000011480888842543826",
            "extra": "mean: 7.230182917831082 usec\nrounds: 20337"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12667681.253680993,
            "unit": "iter/sec",
            "range": "stddev: 8.009233293429473e-9",
            "extra": "mean: 78.94104532433451 nsec\nrounds: 116605"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_5min]",
            "value": 3.6209817165653853,
            "unit": "iter/sec",
            "range": "stddev: 0.06471164005611182",
            "extra": "mean: 276.1681992000035 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_5min]",
            "value": 0.9051345083906909,
            "unit": "iter/sec",
            "range": "stddev: 0.03216475085138001",
            "extra": "mean: 1.1048081702000048 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_30min]",
            "value": 3.161037017263976,
            "unit": "iter/sec",
            "range": "stddev: 0.0694355727448909",
            "extra": "mean: 316.3518789999955 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_15min]",
            "value": 4.729329616940543,
            "unit": "iter/sec",
            "range": "stddev: 0.03002893599855186",
            "extra": "mean: 211.4464587999919 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_5min]",
            "value": 0.9197968669973239,
            "unit": "iter/sec",
            "range": "stddev: 0.018580421123293583",
            "extra": "mean: 1.0871965712000076 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_30min]",
            "value": 4.34570707295179,
            "unit": "iter/sec",
            "range": "stddev: 0.0619841783569886",
            "extra": "mean: 230.1121505000007 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_15min]",
            "value": 2.592898265719891,
            "unit": "iter/sec",
            "range": "stddev: 0.08907557995668701",
            "extra": "mean: 385.6688143999975 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_15min]",
            "value": 2.967130843745561,
            "unit": "iter/sec",
            "range": "stddev: 0.07368167542338279",
            "extra": "mean: 337.0259191999935 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_15min]",
            "value": 5.02765663217819,
            "unit": "iter/sec",
            "range": "stddev: 0.007579560373585273",
            "extra": "mean: 198.89982016666843 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_15min]",
            "value": 4.83362105167257,
            "unit": "iter/sec",
            "range": "stddev: 0.03741218312197121",
            "extra": "mean: 206.88423633333267 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_30min]",
            "value": 3.6034236168142173,
            "unit": "iter/sec",
            "range": "stddev: 0.044563523250963744",
            "extra": "mean: 277.51386079999634 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_60min_5min]",
            "value": 4.966676017725497,
            "unit": "iter/sec",
            "range": "stddev: 0.002283215615207758",
            "extra": "mean: 201.3419028000044 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_1day_30min]",
            "value": 3.8385337189346367,
            "unit": "iter/sec",
            "range": "stddev: 0.04252940485072468",
            "extra": "mean: 260.51614319999885 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_30min]",
            "value": 5.294555565978695,
            "unit": "iter/sec",
            "range": "stddev: 0.0042822242379468925",
            "extra": "mean: 188.87326566666238 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_1day_5min]",
            "value": 0.9538731761340399,
            "unit": "iter/sec",
            "range": "stddev: 0.008190895380735964",
            "extra": "mean: 1.0483573969999953 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2020_60min_5min]",
            "value": 4.768888749518696,
            "unit": "iter/sec",
            "range": "stddev: 0.017992569040934332",
            "extra": "mean: 209.69245719999776 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2025_60min_30min]",
            "value": 5.202633103599397,
            "unit": "iter/sec",
            "range": "stddev: 0.006488590034831679",
            "extra": "mean: 192.21036350000512 msec\nrounds: 6"
          },
          {
            "name": "tests/benchmark/test_ephemeris_benchmark.py::test_benchmark_ephemeris_endpoint_response_time[EPHEMERIS_2024_1day_15min]",
            "value": 2.9254898015342867,
            "unit": "iter/sec",
            "range": "stddev: 0.0817897137907812",
            "extra": "mean: 341.8231023999965 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_tle_data_response_time",
            "value": 3.9159878165380397,
            "unit": "iter/sec",
            "range": "stddev: 0.004958290147980489",
            "extra": "mean: 255.36340939999602 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_get_active_satellites_response_time",
            "value": 0.699622723996481,
            "unit": "iter/sec",
            "range": "stddev: 0.07305218372557999",
            "extra": "mean: 1.429341794800007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_tools_benchmark.py::test_benchmark_tools_tles_at_epoch_response_time",
            "value": 1.1472808280115567,
            "unit": "iter/sec",
            "range": "stddev: 0.06195256765033022",
            "extra": "mean: 871.626175199998 msec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_2010_radius1_duration30]",
            "value": 0.49154602143830284,
            "unit": "iter/sec",
            "range": "stddev: 0.30419924704858536",
            "extra": "mean: 2.034397505800007 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_fov_endpoint_response_time[FOV_radius_10_radius10_duration30]",
            "value": 0.19230130538224802,
            "unit": "iter/sec",
            "range": "stddev: 0.8850303485347615",
            "extra": "mean: 5.2001727082 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 223.48857151359513,
            "unit": "iter/sec",
            "range": "stddev: 0.00026783922889601355",
            "extra": "mean: 4.474501730569111 msec\nrounds: 193"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_horizon_endpoint_response_time[Horizon_2024]",
            "value": 0.2538036643255908,
            "unit": "iter/sec",
            "range": "stddev: 0.1530346766200339",
            "extra": "mean: 3.940053437200004 sec\nrounds: 5"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 93601.2943998627,
            "unit": "iter/sec",
            "range": "stddev: 0.000001844228428860794",
            "extra": "mean: 10.683612939453825 usec\nrounds: 13463"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 18318.69665064289,
            "unit": "iter/sec",
            "range": "stddev: 0.0000058232245846548876",
            "extra": "mean: 54.589036494848294 usec\nrounds: 7179"
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
          "id": "346646886c3655e7b23063f5622ff38b424e1c3b",
          "message": "Update Node version for load testing workflow error",
          "timestamp": "2025-09-05T12:41:19-07:00",
          "tree_id": "aa9557b665a5110a3d8cedb42d53d9e7d2569541",
          "url": "https://github.com/iausathub/satchecker/commit/346646886c3655e7b23063f5622ff38b424e1c3b"
        },
        "date": 1757101558473,
        "tool": "pytest",
        "benches": [
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_complete",
            "value": 220.22655862270057,
            "unit": "iter/sec",
            "range": "stddev: 0.00013744587984004724",
            "extra": "mean: 4.540778397728282 msec\nrounds: 176"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellites_above_horizon_setup",
            "value": 17467.14825800248,
            "unit": "iter/sec",
            "range": "stddev: 0.000008725823092700328",
            "extra": "mean: 57.250329889531656 usec\nrounds: 8809"
          },
          {
            "name": "tests/benchmark/test_fov_benchmark.py::test_benchmark_get_satellite_passes_in_fov_setup",
            "value": 94545.66334730336,
            "unit": "iter/sec",
            "range": "stddev: 0.0000018187230263139228",
            "extra": "mean: 10.576899718040025 usec\nrounds: 13482"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_jd_to_gst",
            "value": 735906.8705873211,
            "unit": "iter/sec",
            "range": "stddev: 4.5220440241559785e-7",
            "extra": "mean: 1.3588675958438985 usec\nrounds: 35233"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_earth_sun_positions",
            "value": 12680500.958629137,
            "unit": "iter/sec",
            "range": "stddev: 8.468233774423771e-9",
            "extra": "mean: 78.86123768002467 nsec\nrounds: 123077"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_is_illuminated",
            "value": 133413.09977408726,
            "unit": "iter/sec",
            "range": "stddev: 0.0000013127109046479598",
            "extra": "mean: 7.495515820360463 usec\nrounds: 14317"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_calculate_lst",
            "value": 675290.6217253872,
            "unit": "iter/sec",
            "range": "stddev: 5.342123631416087e-7",
            "extra": "mean: 1.4808439030960787 usec\nrounds: 39578"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_fov_propagation_strategy",
            "value": 1386.3616393893637,
            "unit": "iter/sec",
            "range": "stddev: 0.00002297374013076152",
            "extra": "mean: 721.3125144175654 usec\nrounds: 867"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_skyfield_propagation",
            "value": 519.0240050842596,
            "unit": "iter/sec",
            "range": "stddev: 0.00008051003160990088",
            "extra": "mean: 1.926693159091279 msec\nrounds: 396"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec_unit_vector",
            "value": 199459.58693362016,
            "unit": "iter/sec",
            "range": "stddev: 8.506483376826006e-7",
            "extra": "mean: 5.013546931353059 usec\nrounds: 44011"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_tle_to_icrf_state",
            "value": 471.3499228697767,
            "unit": "iter/sec",
            "range": "stddev: 0.0001383125151982676",
            "extra": "mean: 2.121566062664398 msec\nrounds: 383"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_icrf2radec",
            "value": 138857.6349563337,
            "unit": "iter/sec",
            "range": "stddev: 0.000001951196334304604",
            "extra": "mean: 7.201620568537468 usec\nrounds: 18475"
          },
          {
            "name": "tests/benchmark/test_util_benchmark.py::test_benchmark_get_phase_angle",
            "value": 160638.17003789282,
            "unit": "iter/sec",
            "range": "stddev: 0.0000010419938387486173",
            "extra": "mean: 6.225170516846094 usec\nrounds: 33117"
          }
        ]
      }
    ]
  }
}