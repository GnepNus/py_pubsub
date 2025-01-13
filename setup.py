from setuptools import setup

package_name = 'py_pubsub'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, 'py_pubsub.test'],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sunpeng',
    maintainer_email='sunpeng@oetsky.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'talker = py_pubsub.publisher_member_function:main',
                'talker2 = py_pubsub.publisher:main',
                'listener = py_pubsub.publisher_member_function:main',
                'listener2 = py_pubsub.subscriber:main',
        ],
    },
)
