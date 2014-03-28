#!/usr/bin/python
from eclipse2buck import config
from eclipse2buck.generator.base_target import BaseTarget

class CreateApk(BaseTarget):
    """
    gen apk target script
    Because of this script is quiet stable, so we will read the template from APP_BUCK.in, and replace the sdk target with project.properties
    """
    template = ""
    def __init__(self, root, name):
        BaseTarget.__init__(self, root, name, config.proj_suffix)
        self._init_template()

    def dump(self):
        print self.template.replace('{%TARGET_SDK%}', self.properties.sdk_target)        
    
    def _init_template(self):
        self.template = """
include_defs('//app/DEFS')
include_defs('//app/SECONDARY_DEX_PATTERN_LIST')
include_defs('//app/PRIMARY_DEX_PATTERN_LIST')

def create_apks(
    name,
    debug_keystore,
    release_keystore
    ):

  # This loop will create two android_binary rules.
  for type in [ 'debug', 'release', 'pre-release' ]:
    # Select the appropriate keystore.
    if type == 'debug':
      keystore = debug_keystore
      linear_size = 8 * 1024 * 1024
      proguard_config = False
    elif type == 'release':
      keystore = release_keystore
      linear_size = 3.5 * 1024 * 1024
      proguard_config = True
    else:
      keystore = release_keystore
      linear_size = 3.5 * 1024 * 1024
      proguard_config = False

    android_binary(
      name = '%s_%s' % (name, type),
      manifest = genfile('AndroidManifest__app_manifest__.xml'),
      android_target = '{%TARGET_SDK%}',
      keystore = keystore,
      package_type = 'release',
      proguard_config = 'proguard.cfg',
      dex_compression = 'jar',
      use_split_dex = True,
      use_linear_alloc_split_dex = True,
      minimize_primary_dex_size = False,
      linear_alloc_hard_limit = linear_size,
      primary_dex_patterns = PRIMARY_DEX_PATTERN_WHITE_LIST,
      secondary_dex_patterns = SECONDARY_DEX_PATTERN_LIST,
      assets_native_library = [
        'libvoipCodec_v5.so', 
        'libvoipCodec_v7a.so', 
        'libvoipCodec.so'
      ],
      deps = [
        ':app_PROJ',
        ':app_manifest',
      ],
      use_android_proguard_config_with_optimizations = proguard_config,
    )
  

create_apks(
  name = 'amm_app_preview',
  debug_keystore = ':debug_keystore',
  release_keystore = ':debug_keystore',
)

android_manifest (
  name = 'app_manifest',
  skeleton = 'AndroidManifest.xml',
  deps = DEPS,
)

keystore(
  name = 'debug_keystore',
  store = 'debug.keystore',
  properties = 'debug.keystore.properties',
)

        """
