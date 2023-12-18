workspace {

    model {
        user = person "Language Learner" "A user that learns language using flashcards on our website." {
            tags "user"
        }

        frontend = softwareSystem "Frontend" "Provides visitors with web interface." {
            tags "frontend"

            iosApp = container "iOS App" "Provides the same functionality as the Single-Page Application." "Swift" {
                tags "iosApp"
                user -> this "Views and creates flashcards using"
            }

            webApplication = container "Web Application" "Provides all of the flashcards functionality to visitors via their web browser." {
                tags "webApplication"
                user -> this "Reads flashcards using"
            }

            androidApp = container "Android App" "Provides the same functionality as the Single-Page Application." "Kotlin" {
                tags "androidApp"
                user -> this "Reads flashcards using"
            }
        }

        apiGateway = softwareSystem "API Gateway" "Provides visitors with ability to view and create flashcards." {
            tags "apiGateway"

            apiApplication = container "API Application" "Implemenths backend-for-frontend pattern via a JSON/HTTPS API." "Python and FastAPI" {
                tags "apiApplication"
                webApplication -> this "Makes API calls to" "JSON/HTTPS"
                iosApp -> this "Makes API calls to" "JSON/HTTPS"
                androidApp -> this "Makes API calls to" "JSON/HTTPS"
            }
        }

        flashcardsSystem = softwareSystem "Flashcards System" "Provides users with their flashcards." {
            tags "flashcardsSystem"

            flashcardsApplication = container "Flashcards Application" "Provides flashcards via a JSON/HTTPS API." "Python and FastAPI" {
                tags "flashcardsApplication"
                apiApplication -> this "Makes API calls to" "JSON/HTTPS"
            }

            flashcardsDatabase = container "Flashcards Database" "Stores flashcards." "Postgres" {
                tags "flashcardsDatabase"
                flashcardsApplication -> this "Reads from and writes to" "SQL/TCP"
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
            include user frontend apiGateway flashcardsSystem userProfilesSystem
            autolayout lr
        }

        container frontend {
            include *
            autolayout lr
        }

        container apiGateway {
            include apiApplication flashcardsApplication userProfileApplication
            autolayout lr
        }

        container apiGateway "and_flashcards" {
            include apiApplication flashcardsApplication flashcardsDatabase
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
            element flashcardsDatabase {
                shape Cylinder
            }
            element userProfilesDatabase {
                shape Cylinder
            }
        }

        theme default
    }

}
