(Используется python 3.7.9)

1.Переходим в папку в командной строке

2.Создаем виртуальное окружение
python3 -m venv pc_env

3. Активируем окружение
На мак: 
source pc_env/bin/activate

На Windows:
cd pc_env/Scripts
activate.ps1 			если из powershell (или activate.bat если из cmd)
cd ../..

4. Устанавливаем библиотеки (нужен git)
pip install numpy
python -m pip install git+https://github.com/DanielPollithy/pypcd.git
brew install gdal
brew install pdal
pip install "laspy[lazrs,laszip]"

5. В shift_rotate.py изменить input_path, output_path, shift_x, shift_y, shift_z, rotation_angle и сохранить

6. Запустить скрипт
python shift_rotate.py



laspy==2.5.0
numpy==1.21.6
pypcd @ git+https://github.com/DanielPollithy/pypcd.git@88ab8c98ab81dd620bf4b22d965b37457aab78f8
python-lzf==0.2.4
