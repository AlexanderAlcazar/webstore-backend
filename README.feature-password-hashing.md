# Feature Branch README: `feature/password-hashing`

This branch upgrades authentication from plain password comparison to hashed password handling.

## Goal

Hash passwords when users register and verify hashes when users log in.

## Why This Branch Exists

The current auth example is intentionally simple, but storing or comparing plain passwords should be replaced before auth is treated as complete.

## Planned Work

- hash passwords before saving new users
- verify the stored hash during login
- keep the implementation simple and readable for MVP scope

## Expected Result

Authentication becomes safer while preserving the same basic register/login flow.

## Likely Files

- `app/services/auth_service.py`
- `app/repositories/user_repository.py`
- auth-related helpers or config if needed

## Merge Back to Main

After this branch is merged, the app keeps MVP auth behavior but uses more realistic password handling.
