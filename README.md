# AD User Lookup (by attribute)
## Installing

Set up the environment,

```
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt

# create the .env file, and fill in the values for the AD_* environment variables.
cp .env.example .env
vim .env
```

## Running

To look up a user by email,

```
python lookup.py mail Example.Person@solidigmtechnology.com
```