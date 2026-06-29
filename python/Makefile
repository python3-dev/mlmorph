all:
	@mkdir -p mlmorph/data
	cp ../malayalam.a mlmorph/data/malayalam.a
	uv sync --extra tests --extra dev

test:
	uv run pytest test/unit/ -v

lint:
	uv run ruff check .
	uv run ruff format --check .

clean:
	@rm -f mlmorph/data/*.a