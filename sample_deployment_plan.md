# Deployment Plan: Customer Portal

- **Date:** Example
- **Environment:** production
- **Application type:** web application
- **Release strategy:** blue-green

## Sample risk register
| Risk | Mitigation |
|---|---|
| Unhealthy release | Use smoke tests and health checks; stop promotion if checks fail. |
| Configuration mismatch | Validate environment configuration and required variables. |
| Customer impact | Use staged traffic rollout where possible and keep an incident owner available. |

## Rollback plan
1. Declare rollback if agreed health checks fail or critical user journeys break.
2. Pause rollout and notify the release owner and incident channel.
3. Switch traffic back to the previous healthy environment and verify routing.
4. Verify service health, core user journeys, logs, and key metrics.
5. Record the timeline, impact, decision, and follow-up actions.

> Example only; tailor all steps to the real system and approved release process.
