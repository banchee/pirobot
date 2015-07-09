package example.com.pirobotcontroller;

import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.IBinder;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;

public class sensorService extends Service implements SensorEventListener {

    SensorManager mSensorManager ;
    Sensor accSensor ;
    String IP_ADDRESS ;
    int PORT_NUMBER ;

    List<Float> co_ordinates = new ArrayList<Float>() ;

    public sensorService() {
        super();
    }

    @Override
    public final void onCreate() {

        super.onCreate();
        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accSensor      = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) ;
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        float[] gravity   = new float[2];
        final float alpha = (float) 0.8;

        Socket dataSocket ;
        DataOutputStream oStream = null;

        // Isolate the force of gravity with the low-pass filter.
        gravity[0] = alpha * gravity[0] + (1 - alpha) * event.values[0];
        gravity[1] = alpha * gravity[1] + (1 - alpha) * event.values[1];
        gravity[2] = alpha * gravity[2] + (1 - alpha) * event.values[2];

        // Remove the gravity contribution with the high-pass filter.
        co_ordinates.set(0, event.values[0] - gravity[0]);
        co_ordinates.set(0, event.values[1] - gravity[1]);
        co_ordinates.set(0, event.values[2] - gravity[2]);

        try {
            dataSocket = new Socket(IP_ADDRESS, PORT_NUMBER);
            oStream    = new DataOutputStream(dataSocket.getOutputStream());
            oStream.writeBytes("x:" + co_ordinates.get(0).toString() + "," + "y:" + co_ordinates.get(1).toString() + "," + "z:" + co_ordinates.get(2).toString());
        } catch (UnknownHostException e){
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public int onStartCommand (Intent intent, int flags, int startId){
        // register listener to the sensors event - this is important
        IP_ADDRESS = intent.getStringExtra("IP_ADDRESS");
        PORT_NUMBER = Integer.parseInt(intent.getStringExtra("PORT_NO"));

        mSensorManager.registerListener(this, accSensor, SensorManager.SENSOR_DELAY_NORMAL);
        return super.onStartCommand(intent,flags,startId);
    }

    @Override
    public void onDestroy () {
        mSensorManager.unregisterListener(this);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null ;
    }


}
