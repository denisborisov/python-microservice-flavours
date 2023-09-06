workspace {

    model {
        articlesReader = person "Articles Reader" "A visitor reading articles on our website." {
            tags "articlesReader"
        }

        frontend = softwareSystem "Frontend" "Provides visitors with web interface." {
            tags "frontend"

            iosApp = container "iOS App" "Provides the same functionality as the Single-Page Application." "Swift" {
                tags "iosApp"
                articlesReader -> this "Reads articles using"
            }

            webApplication = container "Web Application" "Provides all of the Step-By-Step functionality to visitors via their web browser." {
                tags "webApplication"
                articlesReader -> this "Reads articles using"
            }

            androidApp = container "Android App" "Provides the same functionality as the Single-Page Application." "Kotlin" {
                tags "androidApp"
                articlesReader -> this "Reads articles using"
            }
        }

        apiGateway = softwareSystem "API Gateway" "Provides visitors with ability to view and create articles." {
            tags "apiGateway"

            apiApplication = container "API Application" "Provides Step-By-Step functionality via a JSON/HTTPS API." "Python and FastAPI" {
                tags "apiApplication"
                webApplication -> this "Makes API calls to" "JSON/HTTPS"
                iosApp -> this "Makes API calls to" "JSON/HTTPS"
                androidApp -> this "Makes API calls to" "JSON/HTTPS"
            }
        }

        articlesSystem = softwareSystem "Articles System" "Provides users with public and private articles." {
            tags "articlesSystem"

            articlesApplication = container "Articles Application" "Provides articles via a JSON/HTTPS API." "Python and FastAPI" {
                tags "articlesApplication"
                apiApplication -> this "Makes API calls to" "JSON/HTTPS"
            }

            articlesDatabase = container "Articles Database" "Stores articles." "Postgres" {
                tags "articlesDatabase"
                articlesApplication -> this "Reads from and writes to" "SQL/TCP"
            }
        }

        userProfilesSystem = softwareSystem "User Profiles System" "Provides users with their profiles." {
            tags "userProfilesSystem"

            userProfileApplication = container "User Profile Application" "Provides user profile via a JSON/HTTPS API." "Python and FastAPI" {
                tags "userProfileApplication"
                apiApplication -> this "Makes API calls to" "JSON/HTTPS"
            }

            userProfilesDatabase = container "User Profile Database" "Stores user profiles." "Postgres" {
                tags "userProfilesDatabase"
                userProfileApplication -> this "Reads from and writes to" "SQL/TCP"
            }
        }
    }

    views {
        systemContext frontend "Frontend" {
            include articlesReader frontend apiGateway articlesSystem userProfilesSystem
            autolayout lr
        }

        container frontend {
            include *
            autolayout lr
        }

        container apiGateway {
            include apiApplication articlesApplication userProfileApplication
            autolayout lr
        }

        container apiGateway "and_articles" {
            include apiApplication articlesApplication articlesDatabase
            autolayout lr
        }

        container apiGateway "and_user_profiles" {
            include apiApplication userProfileApplication userProfilesDatabase
            autolayout lr
        }

        styles {
            element webApplication {
                shape WebBrowser
            }
            element iosApp {
                shape MobileDevicePortrait
            }
            element androidApp {
                shape MobileDevicePortrait
            }
            element articlesDatabase {
                shape Cylinder
            }
            element userProfilesDatabase {
                shape Cylinder
            }
        }

        theme default
    }

}
