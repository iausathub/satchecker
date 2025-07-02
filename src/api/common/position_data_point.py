from collections import namedtuple

position_data_point = namedtuple(
    "position_data_point",
    [
        "ra",
        "dec",
        "dracosdec",
        "ddec",
        "alt",
        "az",
        "distance",
        "ddistance",
        "phase_angle",
        "illuminated",
        "jd",
        "date_collected",
        "name",
        "catalog_id",
        "data_source",
    ],
)
