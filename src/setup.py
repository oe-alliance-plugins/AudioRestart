from setuptools import setup
import setup_translate

pkg = 'Extensions.AudioRestart'
setup(name='enigma2-plugin-extensions-audiorestart',
       version='3.0',
       description='Restart Audio after restart / standby',
       package_dir={pkg: 'AudioRestart'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo', 'img/button-blue.png', 'img/button-green.png', 'img/button-red.png', 'img/button-yellow.png', 'AudioRestart.png', 'LICENSE', 'maintainer.info']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
