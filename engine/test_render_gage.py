#!/usr/bin/env python3
import sys
from pathlib import Path

# Add project root
root = Path(__file__).resolve().parent.parent.parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from holymoly_studio.engine.flutter_renderer import capture_widget

try:
    out = capture_widget(
        flutter_project_dir="C:/Users/ertyui/ZCodeProject/gage/gage-app",
        widget_import="import 'package:gage_app/features/home/presentation/widgets/service_grid_clay.dart';",
        widget_instantiation="ServiceGridClay(onFoodTap: () {})",
        output_filename="gage_service_grid_typography.png",
        width=412,
        height=220,
        dpr=2.0,
        background_color="0xFFFFFFFF",
    )
    print(f"SUCCESS: Rendered to {out}")
except Exception as e:
    print(f"FAILED: {e}")
