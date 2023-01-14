To run:

```bash
docker build . -t unflipper
docker run -d --rm -e "UNFLIPPER_TOKEN=[token]" --name unflipper unflipper
```