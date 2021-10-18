import dbus, dbus.mainloop.glib, sys
import os
from pocketsphinx import LiveSpeech, get_model_path
from gi.repository import GLib

model_path = get_model_path()
#print(model_path)

def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        elif prop == 'Track':
            print('Music Info:')
            for key in ('Title', 'Artist', 'Album'):
                print('   {}: {}'.format(key, value.get(key, '')))

def on_playback_control(fd,condition):
    str = recognition()
    if str == 'reproducir':
        player_iface.Play()
        return False
    elif str == 'pausa':
        player_iface.Pause()
        return True
    elif str =='siguiente':
        player_iface.Next()
        return True
    elif str =='anterior':
        player_iface.Previous()
        return True
    elif str =='vol':
        vol = int(str.split()[1])
        if vol not in range(0, 128):
            print('Possible Values: 0-127')
            return True
        transport_prop_iface.Set(
                'org.bluez.MediaTransport1',
                'Volume',
                dbus.UInt16(vol))
                
    return True

def recognition():
    speech = LiveSpeech(
		verbose=False,
		sampling_rate=16000,
		buffer_size=2048,
		no_search=False,
		full_utt=False,
		hmm= os.path.join(model_path, 'es-Mx'),
		lm= os.path.join(model_path, 'es-Mx.lm.bin'),
		dict= os.path.join(model_path, 'bocina.dic')
	)

    for phrase in speech:
        print(phrase)
        
        return(str(phrase))

    
	    

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    obj = bus.get_object('org.bluez', "/")
    mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
    player_iface = None
    transport_prop_iface = None
    for path, ifaces in mgr.GetManagedObjects().items():
        if 'org.bluez.MediaPlayer1' in ifaces:
            player_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.bluez.MediaPlayer1')
        elif 'org.bluez.MediaTransport1' in ifaces:
            transport_prop_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.freedesktop.DBus.Properties')
    if not player_iface:
        sys.exit('Error: Media Player not found.')
    if not transport_prop_iface:
        sys.exit('Error: DBus.Properties iface not found.')
    bus.add_signal_receiver(
            on_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties')
    print("a")
    GLib.io_add_watch(sys.stdout, GLib.IO_OUT, on_playback_control)
    GLib.MainLoop().run()