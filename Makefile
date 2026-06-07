.PHONY: format lint check create-env update-env export-simulation export-simulation-linux export-simulation-windows export-simulation-macos simulate

# Optional per-user overrides, e.g. GODOT=/absolute/path/to/Godot
-include .make.local

GODOT ?= godot
SIM_EXPORT_PRESET ?= Linux
SIM_EXPORT_PATH ?= bin/simulation.x86_64
SIM_BINARY ?= simulation/$(SIM_EXPORT_PATH)

format:
	black .

lint:
	ruff check .

check:
	black --check .
	ruff check .

create-env:
	conda env create -f scripts/environment.yml

update-env:
	conda env update -f scripts/environment.yml --name winding

export-simulation:
	mkdir -p simulation/bin
	@GODOT_BIN="$(GODOT)"; \
	case "$$GODOT_BIN" in "~/"*) GODOT_BIN="$$HOME/$${GODOT_BIN#~/}";; esac; \
	if ! command -v "$$GODOT_BIN" >/dev/null 2>&1 && [ ! -x "$$GODOT_BIN" ]; then \
		echo "Godot executable not found: $$GODOT_BIN"; \
		echo "Run with GODOT set to your binary path, e.g."; \
		echo "  make GODOT=/absolute/path/to/Godot export-simulation"; \
		exit 127; \
	fi; \
	cd simulation && "$$GODOT_BIN" --headless --export-release "$(SIM_EXPORT_PRESET)" "$(SIM_EXPORT_PATH)"

export-simulation-linux:
	$(MAKE) export-simulation SIM_EXPORT_PRESET="Linux" SIM_EXPORT_PATH="bin/simulation.x86_64"

export-simulation-windows:
	$(MAKE) export-simulation SIM_EXPORT_PRESET="Windows" SIM_EXPORT_PATH="bin/simulation.exe"

export-simulation-macos:
	$(MAKE) export-simulation SIM_EXPORT_PRESET="macOS" SIM_EXPORT_PATH="bin/simulation.app"

simulate:
	@if [ ! -e "$(SIM_BINARY)" ]; then \
		echo "Simulation binary not found: $(SIM_BINARY)"; \
		echo "Build first with: make export-simulation"; \
		exit 1; \
	fi
	@echo "Launching simulation binary only."
	@echo "Run these in separate terminals:"
	@echo "  python scripts/main.py -s"
	@echo "  python scripts/ws.py"
	@"$(SIM_BINARY)"