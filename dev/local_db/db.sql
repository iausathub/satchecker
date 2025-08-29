CREATE TABLE satellites(
   id serial PRIMARY KEY,
   sat_number INTEGER NOT NULL,
   sat_name TEXT NOT NULL,
   constellation TEXT,
   date_added TIMESTAMPTZ NOT NULL DEFAULT NOW(),
   date_modified TIMESTAMPTZ NOT NULL DEFAULT NOW(),
   rcs_size TEXT,
   launch_date TIMESTAMPTZ,
   decay_date TIMESTAMPTZ,
   object_id TEXT,
   object_type TEXT,
   has_current_sat_number BOOLEAN NOT NULL DEFAULT FALSE,
   generation TEXT,
   UNIQUE (sat_number, sat_name)
);

CREATE TABLE tle(
   id serial PRIMARY KEY,
   sat_id serial NOT NULL,
   date_collected TIMESTAMPTZ NOT NULL,
   tle_line1 TEXT NOT NULL,
   tle_line2 TEXT NOT NULL,
   epoch TIMESTAMPTZ NOT NULL,
   is_supplemental BOOLEAN NOT NULL,
   data_source TEXT NOT NULL default 'spacetrack',
   FOREIGN KEY (sat_id)
      REFERENCES satellites (id),
   UNIQUE (sat_id, epoch, data_source)
);
