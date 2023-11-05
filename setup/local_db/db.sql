CREATE TABLE satellites(
   id serial PRIMARY KEY,
   sat_number INTEGER UNIQUE NOT NULL,
   sat_name TEXT NOT NULL,
   constellation TEXT
);

CREATE TABLE tle(
   id serial PRIMARY KEY,
   sat_id serial NOT NULL,
   date_collected TIMESTAMPTZ NOT NULL,
   tle_line1 TEXT NOT NULL,
   tle_line2 TEXT NOT NULL,
   epoch TIMESTAMPTZ NOT NULL,
   is_supplemental BOOLEAN NOT NULL,
   FOREIGN KEY (sat_id)
      REFERENCES satellites (id),
   UNIQUE (sat_id, epoch)
);

ALTER TABLE public.tle
ADD CONSTRAINT unique_tle UNIQUE (sat_id, epoch);
