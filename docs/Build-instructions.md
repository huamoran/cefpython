# Build instructions

These instructions are for the new releases of CEF Python v50+.
For the old v31 release that is supported on all platforms, see
the build instructions on the wiki pages.

If you would like to quickly build cefpython then see the
[Quick build instructions for Windows](#quick-build-instructions-for-windows)
and [Quick build instructions for Linux](#quick-build-instructions-for-linux)
sections. These instructions are complete meaning you don't need
to read anything more from this document. Using these quick
instructions you should be able to build cefpython in less than
10 minutes.

There are several types of builds described in this document:

1. You can build CEF Python using prebuilt CEF binaries and libraries
   that were uploaded to GH releases
2. You can build CEF Python using prebuilt CEF binaries from
   Spotify Automated Builds.
3. You can build upstream CEF from sources, but note that building CEF
   is a long process that can take hours.

Before you can build CEF Python or CEF you must satisfy
[requirements](#requirements) listed on this page.


Table of contents:
* [Quick build instructions for Windows](#quick-build-instructions-for-windows)
* [Quick build instructions for Linux](#quick-build-instructions-for-linux)
* [Requirements](#requirements)
  * [Windows](#windows)
  * [Linux](#linux)
  * [Mac](#mac)
  * [All platforms](#all-platforms)
* [Build using prebuilt CEF binaries and libraries](#build-using-prebuilt-cef-binaries-and-libraries)
* [Build using CEF binaries from Spotify Automated Builds](#build-using-cef-binaries-from-spotify-automated-builds)
* [Build upstream CEF from sources](#build-upstream-cef-from-sources)
* [Build CEF manually](#build-cef-manually)
* [CEF Automated Builds (Spotify and Adobe)](#cef-automated-builds-spotify-and-adobe)
* [Notes](#notes)
* [How to patch mini tutorial](#how-to-patch-mini-tutorial)


## Quick build instructions for Windows

Complete steps for building CEF Python v50+ using prebuilt binaries
and libraries from GitHub Releases:

1) Tested and works fine on Windows 7 64-bit

2) Download [ninja](https://github.com/ninja-build/ninja) 1.7.2 or later
   and add it to PATH.

3) Download [cmake](https://cmake.org/download/) 3.7.2 or later and add
   it to PATH.

4) For Python 2.7 Install "Visual C++ Compiler for Python 2.7"
  from [here](https://www.microsoft.com/en-us/download/details.aspx?id=44266)

5) For Python 2.7 and when using using "Visual C++ compiler for Python 2.7"
   you have to install "Visual C++ 2008 Redistributable Package (x64)"
   from [here](https://www.microsoft.com/en-us/download/details.aspx?id=15336)

6) Clone cefpython and create a build/ directory and enter it:
```
git clone https://github.com/cztomczak/cefpython.git
cd cefpython/
mkdir build/
cd build/
```

7) Install python dependencies:
```
pip install -r ../tools/requirements.txt
```

8) Download Windows binaries and libraries from
   [GH releases](https://github.com/cztomczak/cefpython/tags)
   tagged e.g. 'v55-upstream' when building v55. The version
   of the binaries must match exactly the CEF version from
   the "cefpython/src/version/cef_version_win.h" file
   (the CEF_VERSION constant).

8) Extract the archive in the "build/" directory.

9) Build cefpython and run examples (xx.x is version number):
```
python ../tools/build.py xx.x
```


## Quick build instructions for Linux

Complete steps for building CEF Python v50+ using prebuilt
binaries and libraries from GitHub Releases:

1) Tested and works fine on Ubuntu 14.04 64-bit

2) Download [ninja](https://github.com/ninja-build/ninja) 1.7.1 or later
   and copy it to /usr/bin and chmod 755.

3) Install required packages (tested and works with: cmake 2.8.12
   and g++ 4.8.4):
```
sudo apt-get install python-dev cmake g++ libgtk2.0-dev
```

4) Clone cefpython and create build/ directory and enter it:
```
git clone https://github.com/cztomczak/cefpython.git
cd cefpython/
mkdir build/
cd build/
```

5) Install python dependencies:
```
sudo pip install -r ../tools/requirements.txt
```

6) Download Linux binaries and libraries from
   [GH releases](https://github.com/cztomczak/cefpython/tags)
   tagged e.g. 'v55-upstream' when building v55. The version
   of the binaries must match exactly the CEF version from
   the "cefpython/src/version/cef_version_linux.h" file
   (the CEF_VERSION constant).

7) Extract the archive in the build/ directory and rename
   the extracted directory to "cef_linux64/".

8) Build cefpython and run examples (xx.x is version number):
```
cd ../src/linux/
python compile.py xx.x
```


## Requirements

Below are platform specific requirements. Do these first before
following instructions in the "All platforms" section that lists
requirements common for all platforms.

### Windows

* Install an appropriate MS compiler for a specific Python version:
  https://wiki.python.org/moin/WindowsCompilers
* For Python 2.7 install "Microsoft Visual C++ Compiler for Python 2.7"
  from [here](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
* When using "Visual C++ compiler for Python 2.7" you have to install
  "Microsoft Visual C++ 2008 Redistributable Package (x64)" from
  [here](https://www.microsoft.com/en-us/download/details.aspx?id=15336)
* To build CEF from sources:
    * Use Win7 x64 or later. 32-bit OS'es are not supported. For more details
     see [here](https://www.chromium.org/developers/how-tos/build-instructions-windows).
    * For CEF branch >= 2704 install VS2015 Update 2 or later. Use the
      Custom Install option, see details [here](https://chromium.googlesource.com/chromium/src/+/master/docs/windows_build_instructions.md#Open-source-contributors).
    * Install [CMake](https://cmake.org/) 2.8.12.1 or newer and add cmake.exe
        to PATH
    * Install [ninja](http://martine.github.io/ninja/) and add ninja.exe
        to PATH
    * You need about 16 GB of RAM during linking. If there is an error
        just add additional virtual memory.
    * For Python 2.7 copy "cefpython/src/windows/stdint.h" to
      "%LocalAppData%\Programs\Common\Microsoft\Visual C++ for Python\9.0\VC\include\"


### Linux

* Install packages: `sudo apt-get install python-dev cmake g++ libgtk2.0-dev`
* If using prebuilt binaries from Spotify automated builds and want to
  build cefclient/cefsimple you need to install these packages:
  `sudo apt-get install libgtkglext1-dev`
* If building CEF from sources:
    * Official binaries are built on Ubuntu 14.04 (cmake 2.8.12, g++ 4.8.4)
    * Download [ninja](http://martine.github.io/ninja/) 1.7.1 or later
      and copy it to /usr/bin and chmod 755.
    * Install required packages using one of the three methods below:
        1. Type command: `sudo apt-get install bison build-essential cdbs curl devscripts dpkg-dev elfutils fakeroot flex g++ git-core git-svn gperf libapache2-mod-php5 libasound2-dev libav-tools libbrlapi-dev libbz2-dev libcairo2-dev libcap-dev libcups2-dev libcurl4-gnutls-dev libdrm-dev libelf-dev libexif-dev libffi-dev libgconf2-dev libgl1-mesa-dev libglib2.0-dev libglu1-mesa-dev libgnome-keyring-dev libgtk2.0-dev libkrb5-dev libnspr4-dev libnss3-dev libpam0g-dev libpci-dev libpulse-dev libsctp-dev libspeechd-dev libsqlite3-dev libssl-dev libudev-dev libwww-perl libxslt1-dev libxss-dev libxt-dev libxtst-dev mesa-common-dev openbox patch perl php5-cgi pkg-config python python-cherrypy3 python-crypto python-dev python-psutil python-numpy python-opencv python-openssl python-yaml rpm ruby subversion ttf-dejavu-core ttf-indic-fonts ttf-kochi-gothic ttf-kochi-mincho fonts-thai-tlwg wdiff zip`
        2. See the list of packages on the
           [cef/AutomatedBuildSetup.md](https://bitbucket.org/chromiumembedded/cef/wiki/AutomatedBuildSetup.md#markdown-header-linux-configuration)
            wiki page.
        2. Run the install-build-deps.sh script -
           instructions provided further down on this page.
    * To build on Debian 7 see
      [cef/BuildingOnDebian7.md](https://bitbucket.org/chromiumembedded/cef/wiki/BuildingOnDebian7.md) and
      [cef/#1575](https://bitbucket.org/chromiumembedded/cef/issues/1575),
      and [cef/#1697](https://bitbucket.org/chromiumembedded/cef/issues/1697)
    * To perform a 32-bit Linux build on a 64-bit Linux system see
      Linux configuration in upstream cef/AutomatedBuildSetup.md. See also
      [cef/#1804](https://bitbucket.org/chromiumembedded/cef/issues/1804).


### Mac

* MacOS 10.9+, Xcode5+ and Xcode command line tools. Only 64-bit builds
  are supported.


### All platforms

* Install dependencies for the automate.py tool by executing:
  `cd tools/ && pip install -r requirements.txt` (on Linux use `sudo`).
  This will install some PyPI packages including Cython.


## Build using prebuilt CEF binaries and libraries

1) Clone cefpython and create a build/ directory and enter it:
```
git clone https://github.com/cztomczak/cefpython.git
cd cefpython/
mkdir build/
cd build/
```

2) Download binaries and libraries from
   [GH releases](https://github.com/cztomczak/cefpython/tags)
   tagged eg. 'v55-upstream' when building v55. The version
   of the binaries must match exactly the CEF version from
   the "cefpython/src/version/" directory (look for CEF_VERSION
   constant in .h file).

3) Extract the downloaded archive eg. "cef55_3.2883.1553.g80bd606_win32.zip"
   in the "build/" directory (using "extract here" option)

4) Run the build.py tool (xx.x is version number):
```
python ../tools/build.py xx.x
```


## Build using CEF binaries from Spotify Automated Builds

1) Clone cefpython and create a build/ directory and enter it:
```
git clone https://github.com/cztomczak/cefpython.git
cd cefpython/
mkdir build/
cd build/
```

2) Download CEF binaries from [Spotify Automated Builds](http://opensource.spotify.com/cefbuilds/index.html).
   The version of the binaries must match exactly the CEF version
   from the "cefpython/src/version/" directory (look for CEF_VERSION
   constant in .h file).

3) Extract the downloaded archive eg.
   "cef_binary_3.2883.1553.g80bd606_windows32.tar.bz2"
   in the build/ directory (using "extract here" option)

4) Run the automate.py tool. After it completes you should see a new
   directory eg. "cef55_3.2883.1553.g80bd606_win32/".
```
python ../tools/automate.py --prebuilt-cef
```

5) Run the build.py tool (xx.x is version number):
```
python ../tools/build.py xx.x
```


## Build upstream CEF from sources

Building CEF from sources is a very long process that can take several
hours depending on your CPU speed and the platform you're building on.
To speed up the process you can pass the --fast-build flag, however
in such case result binaries won't be optimized.
You can optionally set how many parallel ninja jobs to run (by default
cores/2) with the --ninja-jobs flag passed to automate.py.

To build CEF from sources run the automate.py tool using the --build-cef
flag. The automate script will use version information from the
"cefpython/src/version/" directory. If you would like to use
a custom CEF branch
then use the --cef-branch flag, but note that this is only for advanced
users as this will require updating cefpython's C++/Cython code.

If building on Linux and there are errors, see the
"MISSING PACKAGES (Linux)" note futher down.

You should be fine by running automate.py with the default options,
but if you need to customize the build then use the --help flag to
see more options.

The commands below will build CEF from sources with custom CEF Python
patches applied and then build the CEF Python package (xx.x is version
number):
```
git clone https://github.com/cztomczak/cefpython.git
cd cefpython/
mkdir build/
cd build/
python ../tools/automate.py --build-cef --ninja-jobs 6
python ../tools/build.py xx.x
```

The automate.py tool should create eg. "cef55_3.2883.1553.g80bd606_win32/"
directory when it's done. Then the build.py tool will build the cefpython
module, make installer package, install the package and run unit tests
and examples. See the notes for commands for creating package installer
and/or wheel package for distribution.

__MISSING PACKAGES (Linux)__: After the chromium sources are downloaded,
it will try to build cef projects and if it fails due to missing packages
make sure you've installed all the required packages listed in the
Requirements section further up on this page. If it still fails, you
can fix it by running the install-build-deps.sh script (intended for
Ubuntu systems, but you could edit it). When the "ttf-mscorefonts-installer"
graphical installer pops up don't install it - deny EULA.

```
cd build/chromium/src/build/
chmod 755 install-build-deps.sh
sudo ./install-build-deps.sh --no-lib32 --no-arm --no-chromeos-fonts --no-nacl
```

After dependencies are satisifed re-run automate.py.


## Build CEF manually

CEF Python official binaries come with custom CEF binaries with
a few patches applied for our use case, see the Notes section further
down on this page.

On Linux before running any of CEF tools apply the issue73 patch
first.

To build CEF follow the instructions on the Branches and Building
CEF wiki page:
https://bitbucket.org/chromiumembedded/cef/wiki/BranchesAndBuilding

After it is successfully built, apply patches, rebuild and remake
distribs.

Note that CEF patches must be applied in the "download_dir/chromium/src/cef/"
directory, not in the "download_dir/cef/" directory.


## CEF Automated Builds (Spotify and Adobe)

There are two sites that provide automated CEF builds:
* Spotify - http://opensource.spotify.com/cefbuilds/index.html
  * This is the new build system
  * Since June 2016 all builds are without tcmalloc, see
    [cefpython/#73](https://github.com/cztomczak/cefpython/issues/73)
    and [cef/#1827](https://bitbucket.org/chromiumembedded/cef/issues/1827)
* Adobe - https://cefbuilds.com/
  * This is the old build system. Not tested whether it builds without
    tcmalloc.


## Notes

If you would like to update CEF version in cefpython then
see complete instructions provided in
[Issue #264](https://github.com/cztomczak/cefpython/issues/264).

When building for multiple Python versions on Linux/Mac use
pyenv to manage multiple Python installations, see
[Issue #249](https://github.com/cztomczak/cefpython/issues/249)
for details.

Command for making installer package is (xx.x is version number):
```
cd cefpython/build/
python ../tools/make_installer.py xx.x
```

To create a wheel package from that installer package type:
```
cd *-setup/
python setup.py bdist_wheel
cd dist/
ls *.whl
```

Optional flags for the setup.py script above:
* `--python-tag cp27` to generate Python 2.7 only package
* `--universal` to build package for multiple Python versions
  (in such case you must first build multiple cefpython modules
   for each Python version)

CEF Python binaries are build using similar configuration as described
on the ["Automated Build Setup"](https://bitbucket.org/chromiumembedded/cef/wiki/AutomatedBuildSetup.md#markdown-header-platform-build-configurations) wiki page in upstream CEF. The automate.py tool incorporates most of
of the flags from these configurations.

To build the "libcef_dll_wrapper" library type these commands:
```
cd cef_binary*/
mkdir build
cd build/
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release ..
ninja libcef_dll_wrapper
```

To build CEF sample applications type:
```
ninja cefclient cefsimple ceftests
```

Official CEF Python binaries may come with additional patches applied
to CEF/Chromium depending on platform. These patches can be found
in the "cefpython/patches/" directory. Whether you need these patches
depends on your use case, they may not be required and thus you could
use the Spotify Automated Builds. Spotify builds have the issue73 patch
(no tcmalloc) applied.

Currently (February 2017) only Linux releases have the custom
patches applied. Windows and Mac releases use CEF binaries from
Spotify Automated Builds.


## How to patch mini tutorial

Create a patch from unstaged changes in current directory:
```
cd chromium/src/cef/
git diff --no-prefix --relative > issue251.patch
```

Apply a patch in current directory:
```
cd chromium/src/cef/
git apply -v -p0 issue251.patch
```

To create a patch from last two commits (no --relative flag available
in this case, so must be in root CEF dir):
```
git format-patch --no-prefix -2 HEAD --stdout > issue251.patch
```
