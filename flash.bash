sudo umount /media/adhoc/CIRCUITPY
sudo rm -rf /media/adhoc/CIRCUITPY


sudo mkdir -p /media/adhoc/CIRCUITPY/

if ! [[ -e /dev/sda1 ]]
then
    echo "Could not detect /dev/sda1"
    exit 1
fi

if ! sudo mount /dev/sda1 /media/adhoc/CIRCUITPY
then
    echo "Failed to mount /dev/sda1."
    exit 1
fi

sudo rm /media/adhoc/CIRCUITPY/code.py
sudo cp code.py /media/adhoc/CIRCUITPY/
echo "Flashed to Pico."

