from setuptools import find_packages, setup

package_name = 'moveIt'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='rokaia.moh.a@gmail.com',
    description='Kinematics and odometry package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wheel_odometry_node = moveIt.wheel_odometry_node:main',
            'kinematics_node = moveIt.kinematics_node:main',
        ],
    },
)
