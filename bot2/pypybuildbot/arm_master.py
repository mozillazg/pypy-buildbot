from buildbot.scheduler import Nightly, Triggerable
from pypybuildbot.util import load, isRPython
from buildbot.changes import filter

pypybuilds = load('pypybuildbot.builds')
ARMCrossLock = pypybuilds.ARMCrossLock
ARMBoardLock = pypybuilds.ARMBoardLock

# ARM own test factories
jit_translation_args = ['-Ojit']
crosstranslationargs = ['--platform=arm', '--gcrootfinder=shadowstack']
crosstranslationjitargs = ['--jit-backend=arm']
# this one needs a larger timeout due to how it is run
pypyJitBackendOnlyRPythonTestFactoryARM = pypybuilds.RPython(
        cherrypick=':'.join(["jit/backend/arm",
                            "jit/backend/llsupport",
                            "jit/backend/test",  # kill this one in case it is too slow
                            ]),
        timeout=36000)
pypyJitOnlyRPythonTestFactoryARM = pypybuilds.RPython(cherrypick="jit", timeout=2 * 3600)
pypyOwnTestFactoryARM = pypybuilds.Own(timeout=2 * 3600)
pypyRPythonTestFactoryARM = pypybuilds.RPython(timeout=2 * 3600)

pypyCrossTranslationFactoryARM = pypybuilds.NightlyBuild(
    translationArgs=crosstranslationargs + ['-O2'],
    platform='linux-armel',
    interpreter='pypy',
    prefix=['schroot', '-c', 'armel', '--'])

pypyJITCrossTranslationFactoryARM = pypybuilds.NightlyBuild(
    translationArgs=(crosstranslationargs
                        + jit_translation_args
                        + crosstranslationjitargs),
    platform='linux-armel',
    interpreter='pypy',
    prefix=['schroot', '-c', 'armel', '--'],
    trigger='JITLINUXARM_scheduler')

pypyCrossTranslationFactoryRaspbianHF = pypybuilds.NightlyBuild(
    translationArgs=crosstranslationargs + ['-O2'],
    platform='linux-armhf-raspbian',
    interpreter='pypy',
    prefix=['schroot', '-c', 'raspbian', '--'],
    trigger='APPLVLLINUXARMHF_RASPBIAN_scheduler')

pypyJITCrossTranslationFactoryRaspbianHF = pypybuilds.NightlyBuild(
    translationArgs=(crosstranslationargs
                        + jit_translation_args
                        + crosstranslationjitargs),
    platform='linux-armhf-raspbian',
    interpreter='pypy',
    prefix=['schroot', '-c', 'raspbian', '--'],
    trigger='JITLINUXARMHF_RASPBIAN_scheduler')

pypyARMJITTranslatedTestFactory = pypybuilds.TranslatedTests(
    translationArgs=(crosstranslationargs
                        + jit_translation_args
                        + crosstranslationjitargs),
    lib_python=True,
    pypyjit=True,
    app_tests=True,
    platform='linux-armel',
    )
pypyARMTranslatedAppLevelTestFactory = pypybuilds.TranslatedTests(
    translationArgs=crosstranslationargs + ['-O2'],
    lib_python=True,
    app_tests=True,
    platform='linux-armel',
)

pypyARMHF_RASPBIAN_JITTranslatedTestFactory = pypybuilds.TranslatedTests(
    translationArgs=(crosstranslationargs
                        + jit_translation_args
                        + crosstranslationjitargs),
    lib_python=True,
    pypyjit=True,
    app_tests=True,
    platform='linux-armhf-raspbian',
    )
pypyARMHF_RASPBIAN_TranslatedAppLevelTestFactory = pypybuilds.TranslatedTests(
    translationArgs=crosstranslationargs + ['-O2'],
    lib_python=True,
    app_tests=True,
    platform='linux-armhf-raspbian',
)

#
LINUXARMHFOWN = "own-linux-armhf"
LINUXARMHFRPYTHON = "rpython-linux-armhf"
# APPLVLLINUXARM = "pypy-c-app-level-linux-armel"
APPLVLLINUXARMHF_v7 = "pypy-c-app-level-linux-armhf-v7"
# APPLVLLINUXARMHF_RASPBIAN = "pypy-c-app-level-linux-armhf-raspbian"

# JITLINUXARM = "pypy-c-jit-linux-armel"
JITLINUXARMHF_v7 = "pypy-c-jit-linux-armhf-v7"
JITLINUXARMHF_RASPBIAN = "pypy-c-jit-linux-armhf-raspbian"

# JITBACKENDONLYLINUXARMEL = "jitbackendonly-own-linux-armel"
JITBACKENDONLYLINUXARMHF = "jitbackendonly-own-linux-armhf"
JITBACKENDONLYLINUXARMHF_v7 = "jitbackendonly-own-linux-armhf-v7"

# build only
BUILDLINUXARM = "build-pypy-c-linux-armel"
# BUILDJITLINUXARM = "build-pypy-c-jit-linux-armel"
BUILDLINUXARMHF_RASPBIAN = "build-pypy-c-linux-armhf-raspbian"
BUILDJITLINUXARMHF_RASPBIAN = "build-pypy-c-jit-linux-armhf-raspbian"

builderNames = [
    # APPLVLLINUXARM,
    APPLVLLINUXARMHF_v7,
    # APPLVLLINUXARMHF_RASPBIAN,
    # JITLINUXARM,
    JITLINUXARMHF_v7,
    JITLINUXARMHF_RASPBIAN,
    # JITBACKENDONLYLINUXARMEL,
    JITBACKENDONLYLINUXARMHF,
    JITBACKENDONLYLINUXARMHF_v7,
    #BUILDLINUXARM,
    #BUILDJITLINUXARM,
    #BUILDLINUXARMHF_RASPBIAN,
    #BUILDJITLINUXARMHF_RASPBIAN,
]

schedulers = [
    Nightly("nighly-arm-0-00", [
        #BUILDJITLINUXARM,              # on hhu-cross-armel, uses 1 core
        #BUILDJITLINUXARMHF_RASPBIAN,   # on hhu-cross-raspbianhf, uses 1 core

        #BUILDLINUXARM,                 # on hhu-cross-armel, uses 1 core
        #BUILDLINUXARMHF_RASPBIAN,      # on hhu-cross-raspbianhf, uses 1 core

        ], branch='main', hour=0, minute=0,
        onlyIfChanged=True,
    ),

    Nightly("nightly-arm-3-00-py3.5", [
        #BUILDJITLINUXARM,              # on hhu-cross-armel, uses 1 core
        #BUILDJITLINUXARMHF_RASPBIAN,   # on hhu-cross-raspbianhf, uses 1 core
        ], branch="py3.5", hour=3, minute=0,
        #onlyIfChanged=True,
    ),

    Nightly("nightly-arm-0-01", [
        # JITBACKENDONLYLINUXARMEL,      # on hhu-imx.53
        JITBACKENDONLYLINUXARMHF,
        JITBACKENDONLYLINUXARMHF_v7,   # on cubieboard-bob
        ], branch='main', hour=0, minute=0, onlyIfChanged=True,
        fileIsImportant=isRPython,
        change_filter=filter.ChangeFilter(branch='main'),
    ),

    #Triggerable("APPLVLLINUXARM_scheduler", [
    #    APPLVLLINUXARM,            # triggered by BUILDLINUXARM, on hhu-beagleboard
    #]),

    #Triggerable("JITLINUXARM_scheduler", [
    #    JITLINUXARM,               # triggered by BUILDJITLINUXARM, on hhu-beagleboard
    #]),
    Triggerable("APPLVLLINUXARMHF_RASPBIAN_scheduler", [
        # APPLVLLINUXARMHF_RASPBIAN,  # triggered by BUILDLINUXARMHF_RASPBIAN
        APPLVLLINUXARMHF_v7,        # triggered by BUILDLINUXARMHF_RASPBIAN, on cubieboard-bob
    ]),

    Triggerable("JITLINUXARMHF_RASPBIAN_scheduler", [
        JITLINUXARMHF_RASPBIAN,       # triggered by BUILDJITLINUXARMHF_RASPBIAN
        JITLINUXARMHF_v7,             # triggered by BUILDJITLINUXARMHF_RASPBIAN, on cubieboard-bob
    ]),

]

builders = [
  # ARM
  # armel
  ## armv7
  #{"name": JITBACKENDONLYLINUXARMEL,
  # "slavenames": ['hhu-i.mx53'],
  # "builddir": JITBACKENDONLYLINUXARMEL,
  # "factory": pypyJitBackendOnlyRPythonTestFactoryARM,
  # "category": 'linux-armel',
  # "locks": [ARMBoardLock.access('counting')],
  # },
  # armhf
  ## armv6
  {"name": JITBACKENDONLYLINUXARMHF,
   "slavenames": ['hhu-raspberry-pi', 'hhu-pypy-pi', 'hhu-pypy-pi2'],
   "builddir": JITBACKENDONLYLINUXARMHF,
   "factory": pypyJitBackendOnlyRPythonTestFactoryARM,
   "category": 'linux-armhf',
   "locks": [ARMBoardLock.access('counting')],
   },
  ## armv7
  {"name": JITBACKENDONLYLINUXARMHF_v7,
   "slavenames": ['cubieboard-bob'],
   "builddir": JITBACKENDONLYLINUXARMHF_v7,
   "factory": pypyJitBackendOnlyRPythonTestFactoryARM,
   "category": 'linux-armhf',
   "locks": [ARMBoardLock.access('counting')],
   },
  # app level builders
  ## armv7 softfloat
  #{"name": APPLVLLINUXARM,
  # "slavenames": ["hhu-beagleboard"],
  # "builddir": APPLVLLINUXARM,
  # "factory": pypyARMTranslatedAppLevelTestFactory,
  # "category": "linux-armel",
  # "locks": [ARMBoardLock.access('counting')],
  # },
  #{"name": JITLINUXARM,
  # "slavenames": ["hhu-beagleboard"],
  # 'builddir': JITLINUXARM,
  # 'factory': pypyARMJITTranslatedTestFactory,
  # 'category': 'linux-armel',
  # "locks": [ARMBoardLock.access('counting')],
  # },
  ## armv6 hardfloat
  #{"name": APPLVLLINUXARMHF_RASPBIAN,
  # "slavenames": ['hhu-raspberry-pi', 'hhu-pypy-pi', 'hhu-pypy-pi2'],
  # "builddir": APPLVLLINUXARMHF_RASPBIAN,
  # "factory": pypyARMHF_RASPBIAN_TranslatedAppLevelTestFactory,
  # "category": "linux-armhf",
  # "locks": [ARMBoardLock.access('counting')],
  # },
  {"name": JITLINUXARMHF_RASPBIAN,
   "slavenames": ['hhu-raspberry-pi', 'hhu-pypy-pi', 'hhu-pypy-pi2'],
   'builddir': JITLINUXARMHF_RASPBIAN,
   'factory': pypyARMHF_RASPBIAN_JITTranslatedTestFactory,
   'category': 'linux-armhf',
   "locks": [ARMBoardLock.access('counting')],
   },
  ## armv7 hardfloat
  {"name": APPLVLLINUXARMHF_v7,
   "slavenames": ["cubieboard-bob"],
   "builddir": APPLVLLINUXARMHF_v7,
   "factory": pypyARMHF_RASPBIAN_TranslatedAppLevelTestFactory,  # XXX replace this with a custom build
   "category": "linux-armhf",
   "locks": [ARMBoardLock.access('counting')],
   },
  {"name": JITLINUXARMHF_v7,
   "slavenames": ["cubieboard-bob"],
   'builddir': JITLINUXARMHF_v7,
   'factory': pypyARMHF_RASPBIAN_JITTranslatedTestFactory,  # XXX replace this with a custom build
   'category': 'linux-armhf',
   "locks": [ARMBoardLock.access('counting')],
   },
  # Translation Builders for ARM - disabled
  # {"name": BUILDLINUXARM,
  #  "slavenames": ['hhu-cross-armel'],
  #  "builddir": BUILDLINUXARM,
  #  "factory": pypyCrossTranslationFactoryARM,
  #  "category": 'linux-armel',
  #  "locks": [ARMCrossLock.access('counting')],
  #  },
  # {"name": BUILDJITLINUXARM,
  #  "slavenames": ['hhu-cross-armel'],
  #  "builddir": BUILDJITLINUXARM,
  #  "factory": pypyJITCrossTranslationFactoryARM,
  #  "category": 'linux-armel',
  #  "locks": [ARMCrossLock.access('counting')],
  # },
  # {"name": BUILDLINUXARMHF_RASPBIAN,
  #  "slavenames": ['hhu-cross-raspbianhf'],
  #  "builddir": BUILDLINUXARMHF_RASPBIAN,
  #  "factory": pypyCrossTranslationFactoryRaspbianHF,
  #  "category": 'linux-armhf',
  #  "locks": [ARMCrossLock.access('counting')],
  #  },
  # {"name": BUILDJITLINUXARMHF_RASPBIAN,
  #  "slavenames": ['hhu-cross-raspbianhf'],
  #  "builddir": BUILDJITLINUXARMHF_RASPBIAN,
  #  "factory": pypyJITCrossTranslationFactoryRaspbianHF,
  #  "category": 'linux-armhf',
  #  "locks": [ARMCrossLock.access('counting')],
  # },
]
