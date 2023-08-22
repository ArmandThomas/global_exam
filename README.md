
# Install chrome for testing 
(to use only a specific version and not be affected by updates)

Use this command to create a folder with chrome version 114 in it
```bash
npx @puppeteer/browsers install chrome@114 
```

# Install project

## Install requirements

```bash
pip install -r requirements.txt
```

## Copy and edit .env.local

```sh
cp .env .env.local
```

## Start the app

```bash
python main.py
```