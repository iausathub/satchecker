@startuml
!define C4P https://raw.githubusercontent.com/RicardoNiepel/C4-PlantUML/master/C4_Component.puml
!include C4P

LAYOUT_WITH_LEGEND()

title Satellite Data Systems - Component Diagram

Person(Client, "User", "Interacts with the system")

System_Boundary(SatChecker, "SatChecker API") {
    ComponentDb(shared_Database, "Database", "PostgreSQL", "Stores all data")
    ComponentQueue(shared_Cache, "Cache", "Redis", "Stores cached data")

    Container_Boundary(ephem, "Ephemeris") {
        Component(ephem_Routes, "Ephemeris Routes", "Flask", "Handles HTTP requests for ephemeris data")
        Component(ephem_ValidationService, "Input Validation Service", "Flask", "Validates request parameters")
        Component(ephem_EphemerisService, "Ephemeris Service", "Flask", "Generates ephemeris data")
        Component(ephem_TLERepository, "TLE Repository", "Retrieves TLE data")
        Component(ephem_Tasks, "Ephemeris Tasks", "Celery", "Handles async tasks for ephemeris generation")
    }

    Container_Boundary(fov, "Field of View") {
        Component(fov_Routes, "Field of View Routes", "Flask", "Handles HTTP requests for field of view")
        Component(fov_FovService, "Field of View Service", "Python", "Calculates satellites passing through a field of view")
    }

    Container_Boundary(info, "Satellite Info") {
        Component(info_Routes, "Satellite Info Routes", "Flask", "Handles HTTP requests for satellite info")
        Component(info_InfoService, "Satellite Info Service", "Python", "Provides general info on satellites")
    }

    Container_Boundary(alert, "Alerts") {
        Component(alert_Routes, "Alert Routes", "Flask", "Handles HTTP requests for alerts")
        Component(alert_NotificationService, "Notification Service", "Python", "Sends alerts for satellite flares/passes")
    }
}

Rel(Client, ephem_Routes, "GET /ephemeris", "HTTP")
Rel(Client, info_Routes, "GET /tools", "HTTP")
Rel(Client, fov_Routes, "GET /fov", "HTTP")
Rel(Client, alert_Routes, "GET /alerts", "HTTP")

Rel(ephem_Routes, ephem_ValidationService, "Validate parameters")
Rel(ephem_Routes, ephem_EphemerisService, "Get ephemeris (by name/id)")
Rel(ephem_EphemerisService, ephem_TLERepository, "Get TLE (by name/id)")
Rel(ephem_TLERepository, shared_Database, "Retrieve TLE data")
Rel(ephem_EphemerisService, ephem_Tasks, "Generate ephemeris data (async)")
Rel(ephem_Tasks, shared_Cache, "Store ephemeris data in cache")

Rel(info_Routes, info_InfoService, "Get satellite info")
Rel(info_InfoService, shared_Database, "Retrieve satellite info")

Rel(fov_Routes, fov_FovService, "Calculate field of view")
Rel(fov_FovService, shared_Database, "Retrieve field of view data")
Rel(fov_FovService, ephem_EphemerisService, "Get satellite pass info")
Rel(fov_FovService, ephem_ValidationService, "Validate parameters")

Rel(alert_Routes, alert_NotificationService, "Send alert for satellite flare/pass")
Rel(alert_NotificationService, shared_Database, "Retrieve alert settings")

@enduml
