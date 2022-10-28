organizationFolder("localhost") {
    configure { node ->
        def templates = node / 'properties' / 'jenkins.branch.OrganizationChildTriggersProperty' / templates
        templates << "com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger" {
            spec("* * * * *")
            interval("1m")
        }
    }
    organizations {
        fromSource {
            name("repository")
            sources {
                git {
                    remote("/var/jenkins/repository")
                    traits {
                        gitBranchDiscovery()
                    }
                }
            }
        }
    }
    triggers {
        cron {
            spec("* * * * *")
        }
        periodicFolderTrigger {
            interval("1m")
        }
    }
}

organizationFolder("github") {
    configure { node ->
        def templates = node / 'properties' / 'jenkins.branch.OrganizationChildTriggersProperty' / templates
        templates << "com.cloudbees.hudson.plugins.folder.computed.PeriodicFolderTrigger" {
            spec("* * * * *")
            interval("60m")
        }
    }
    organizations {
        fromSource {
            name("${GITHUB_USERNAME} » ${GITHUB_REPOSITORY}")
            sources {
                github {
                    configuredByUrl(true)
                    credentialsId("github-access-token")
                    repository("${GITHUB_REPOSITORY}")
                    repositoryUrl("https://github.com/${GITHUB_USERNAME}/${GITHUB_REPOSITORY}")
                    repoOwner("${GITHUB_USERNAME}")
                    traits {
                        // 1 - discover all branches, except branches that are pull request sources
                        // 2 - discover only branches that are pull request sources
                        // 3 - discover all branches
                        gitHubBranchDiscovery{ strategyId(1) }
                    }
                }
            }
        }
    }
    triggers {
        cron {
            spec("* * * * *")
        }
        periodicFolderTrigger {
            interval("60m")
        }
    }
}
