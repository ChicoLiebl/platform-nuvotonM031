# Modified version of [nuvoton_nuc131](https://github.com/fazerxlo/nuvoton_nuc131) PlatformIO Platform for Nuvoton M031/M032 Series Microcontrollers

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This project provides a custom PlatformIO platform for developing on Nuvoton M031 series microcontrollers, specifically targeting the M032LD2AE. This is heavily based on [nuvoton_nuc131](https://github.com/fazerxlo/nuvoton_nuc131) 

**Note:** This project is currently under development. The build system is functional, but only simple test code was run on microcontroller. Upload was done using Nuvoton Command line Tools under wine (Nulink.exe).

## Features

*   **PlatformIO Integration:** Seamlessly integrates with the PlatformIO IDE and build system.
*   **Nuvoton M031BSP:** Includes the necessary header files and source files from the Nuvoton M031 Board Support Package (BSP) for direct hardware access.
*   **Bare-metal Development:** Designed for bare-metal programming, giving you fine-grained control over the microcontroller.
*   **Map File Generation:** Generates a linker map file (`.map`) for memory usage analysis and debugging.
*   **Garbage Collection:** Uses linker flags (`--gc-sections`) to remove unused code and minimize firmware size.
*   **Example Project:** Includes a basic "blink" example to demonstrate the platform's functionality.

## Project Structure

```
nuvoton/
├── boards/
│   └── nuvoton_m032ld.json  <- Board definition (M032LD2AE)
├── bsp/                      <- Nuvoton M031 BSP files
│   ├── CMSIS/Core/              <- CMSIS core files
│   │   └── Include/
│   │       └── ...
│   ├── Device/             <- Nuvoton device-specific files
│   │   └── M031/
│   │       └── Include/
│   │           └── ...
│   │       └── Source/     <- Startup code and system files
│   │           └── GCC/    <- startup files
│   │           └── ...
│   └── StdDriver/         <- Nuvoton Standard Driver files
│       └── inc/
│           └── ...
│       └── src/
│           └── ...
├── builder/
│   └── main.py             <- PlatformIO build script
├── examples/
│   └── blink/              <- Example "blink" project
│       └── src/
│           └── main.c
├── platform.json           <- Platform manifest
└── platform_nuvoton.py     <- Platform class
```

## Prerequisites

*   **PlatformIO:**  Install PlatformIO Core or the PlatformIO IDE.
*   **Nuvoton M031BSP:**  The BSP files are included in this repository within the `bsp` directory. You should *not* need to download them separately.  If you need a different version of the BSP, you can obtain it from the official Nuvoton website (see Referenced Materials).
*   **ARM GCC Toolchain:**  The platform uses the `toolchain-gccarmnoneeabi` package, which PlatformIO will automatically download and manage.

## Usage

1.  **Clone this Repository:**

    ```bash
    git clone https://github.com/ChicoLiebl/platform-nuvotonM031
    ```

2.  **Place the `nuvoton` directory:** Copy the entire `nuvoton` directory into your PlatformIO platforms directory.  The location of this directory depends on your operating system and PlatformIO installation:
    *   **Linux/macOS:**  `~/.platformio/platforms/`
    *   **Windows:**  `%USERPROFILE%\.platformio\platforms\`
     Alternatively, for development purposes, you can keep the nuvoton folder, where it is, and change platform = path/to/nuvoton in platformio.ini in the examples.

3.  **Create a New PlatformIO Project:**  In the PlatformIO IDE or using the PlatformIO CLI, create a new project.

4.  **Configure `platformio.ini`:**  In your project's `platformio.ini` file, set the following:

    ```ini
    [env:nuvoton_m031]
    platform = nuvoton  ; Or path/to/nuvoton if you placed the directory to another location
    board = nuvoton_m032ld
    ; No framework is explicitly specified for bare-metal development
    ; Optional: upload_port = COM3  ; Replace COM3 with your device's port
    ; Add other upload-related options here as needed by your uploader
    ```

5.  **Write Your Code:**  Create your application code in the `src` directory of your project.  You can use the provided `examples/blink` project as a starting point.  Include the necessary Nuvoton header files (e.g., `NuMicro.h`) to access peripherals and registers.

6.  **Build the Project:**  Use PlatformIO's "Build" command (either in the IDE or via the CLI) to compile your project.

7.  **Upload :** Upload was done using Nuvoton Command line Tools under wine (Nulink.exe). [NuMicro NuLink Command Tool 3.21.7829r](https://www.nuvoton.com/tool-and-software/software-tool/programmer-tool/). Uploading with `tool-nuvoton-isp` or OpenOCD was no yet teste with this package.



## Referenced Materials


*   **Base Project:**
*   *   [nuvoton_nuc131](https://github.com/fazerxlo/nuvoton_nuc131)
*   **PlatformIO Documentation:**
    *   [Creating Custom Platforms](https://docs.platformio.org/en/latest/platforms/creating_platform.html)
    *   [PlatformIO Packages](https://docs.platformio.org/en/latest/core/userguide/pkg/index.html)
*   **Nuvoton Resources:**
    *   [M031 Series Page](https://www.nuvoton.com/products/microcontrollers/arm-cortex-m0-mcus/m031-series/)
    *   [M031BSP (GitHub)](https://github.com/OpenNuvoton/M031BSP) - *Note:* The BSP is already included in this repository, but you can refer to the official repository for updates or different versions.
* **Examples and discussions**
	* [PlatformIO Community Discussion](https://community.platformio.org/t/nuvoton-cortex-m-arm-cpu-infrastructure-support/36164)


## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for details.

