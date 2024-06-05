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
python3 -m pip install git+https://github.com/DanielPollithy/pypcd.git
brew install gdal
brew install pdal
pip install "laspy[lazrs,laszip]"

5. В main.py изменить input_path, output_path, shift_x, shift_y, shift_z, rotation_angle и сохранить

6. Запустить скрипт
python main.py
