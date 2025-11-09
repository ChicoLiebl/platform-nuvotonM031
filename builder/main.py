import os
import shutil
from os.path import join
from SCons.Script import *

env = DefaultEnvironment()

# --- Helper Functions ---

def add_includes(env, include_paths):
    """Adds include paths to the environment."""
    for path in include_paths:
        env.Append(CPPPATH=[path])

def add_sources(env, build_dir, src_dir):
    """Adds source files to the build."""
    print(f"Adding sources to {src_dir}")
    env.BuildSources(build_dir, src_dir)

def add_defines(env, defines):
    """Adds preprocessor definitions to the environment."""
    for define in defines:
        env.Append(CPPDEFINES=[define])

# --- Copy BSP Directory (NEW FUNCTION) ---

def copy_bsp(env):
    """Copies the BSP directory to the build directory."""
    platform_dir = env.PioPlatform().get_dir() # Get platform dir
    bsp_src_dir = os.path.join(platform_dir, "bsp")
    build_dir = env.get("PROJECT_BUILD_DIR")
    pioenvv = env.get("PIOENV")
    print(build_dir)
    bsp_dest_dir = os.path.join(build_dir, "bsp")

    if os.path.exists(bsp_src_dir):
        if os.path.exists(bsp_dest_dir):
            shutil.rmtree(bsp_dest_dir)  # Clean previous copy
        shutil.copytree(bsp_src_dir, bsp_dest_dir)
        print(f"Copied 'bsp' directory to {bsp_dest_dir}")
    else:
        print(f"Warning: 'bsp' directory not found in {bsp_src_dir}")

    # env.BuildSources(build_dir, os.path.join(bsp_src_dir, "Device", "M031"))
    # env.BuildSources(build_dir, os.path.join(bsp_src_dir, "StdDriver", "src"))


def build_bsp(env):
    platform_dir = env.PioPlatform().get_dir() # Get platform dir
    build_dir = env.get("PROJECT_BUILD_DIR")
    bsp_src_dir = os.path.join(platform_dir, "bsp")
    bsp_dest_dir = os.path.join(build_dir, "bsp")

    env.BuildSources(os.path.join(build_dir, "Device"), os.path.join(bsp_src_dir, "Device", "M031", "Source"))
    env.BuildSources(os.path.join(build_dir, "StdDriver"), os.path.join(bsp_src_dir, "StdDriver", "src"))
    # env.BuildSources(build_dir, os.path.join(bsp_src_dir, "StdDriver", "src"))
# --- Main Build Script ---

# Call the function to copy the BSP
copy_bsp(env)

env.Replace(
    AR="arm-none-eabi-gcc-ar",
    AS="arm-none-eabi-as",
    CC="arm-none-eabi-gcc",
    CXX="arm-none-eabi-g++",
    GDB="arm-none-eabi-gdb",
    OBJCOPY="arm-none-eabi-objcopy",
    RANLIB="arm-none-eabi-gcc-ranlib",
    SIZETOOL="arm-none-eabi-size",
)


env.Replace(
    CCFLAGS=[
        "-std=gnu11",
        "-Wall",
        "-march=armv6-m",
        "-D__M031__",
        "-Wl,--verbose"
    ],
    LINKFLAGS=[
        "-mcpu=cortex-m0",
        "-specs=nano.specs",
        "-specs=nosys.specs",
        "-Wl,-Map=" + join("$BUILD_DIR", "${PROGNAME}.map"),
        "-Wl,--gc-sections",
        "-lnosys"
    ],
    CFLAGS = [

    ],
    CXXFLAGS=[
      "-std=gnu++14"
    ]
)

env.Append(

    LIBS=[
      "c",
      "gcc"
    ],

    BUILDERS=dict(
        ElfToBin=Builder(
            action=" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "$SOURCES",
                "$TARGET"]),
            suffix=".bin"
        )
    )
)

# --- BSP Integration ---

# 1. Include Paths
bsp_include_paths = [
    join("$PROJECT_BUILD_DIR", "bsp", "CMSIS", "Core", "Include"),     # Use $BUILD_DIR
    # join("$PROJECT_BUILD_DIR", "bsp", "CMSIS", "Core", "Include", "a-profile"),     # Use $BUILD_DIR
    # join("$PROJECT_BUILD_DIR", "bsp", "CMSIS", "Core", "Include", "m-profile"),     # Use $BUILD_DIR
    # join("$PROJECT_BUILD_DIR", "bsp", "CMSIS", "Core", "Include", "r-profile"),     # Use $BUILD_DIR
    join("$PROJECT_BUILD_DIR", "bsp", "Device", "M031", "Include"),  # Use $BUILD_DIR
    join("$PROJECT_BUILD_DIR", "bsp", "StdDriver", "inc")   # Use $BUILD_DIR
]
add_includes(env, bsp_include_paths)

build_bsp(env)

# 2. Source Files
# add_sources(env,
#     os.path.join(env['BUILD_DIR'], "bsp", "Device", "M031"),
#     os.path.join(env['BUILD_DIR'], "bsp", "Device", "M031", "Source"))

# add_sources(env,
#     os.path.join(env['BUILD_DIR'], "bsp", "StdDriver"),
#     os.path.join(env['BUILD_DIR'], "bsp", "StdDriver", "src"))

# add_sources(env,
#     os.path.join(env['BUILD_DIR'], "bsp", "Device", "M031", "Startup"),
#     os.path.join(env['BUILD_DIR'], "bsp", "Device", "M031", "Source", "GCC"))
# Add startup files here if not already included


# 3. Preprocessor Definitions (if needed)
bsp_defines = [
    # Add BSP-specific defines here, if any
]
add_defines(env, bsp_defines)

# --- Build Program ---

target_elf = env.BuildProgram()

#
# Target: Build the .bin file
#
target_bin = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Upload firmware
#
# upload = env.Alias(["upload"], target_bin, "$UPLOADCMD")

#
# Target: Define targets
#
Default(target_bin)