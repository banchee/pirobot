package example.com.pirobotcontroller;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;


public class HomeScreen extends Activity implements SensorEventListener{

    Button btnStart, btnStop ;
    Intent ss;

    boolean lRunSensor = false;

    TextView LogTextView;

    SensorManager mSensorManager ;
    Sensor accSensor ;
    String IP_ADDRESS ;
    int PORT_NUMBER ;

    long lastUpdate ;

    List<Float> co_ordinates = new ArrayList<Float>() ;

    Socket dataSocket ;
    DataOutputStream oStream = null;

    public HomeScreen() {
        super();

    }

    @Override
    public void onPause(){
        super.onPause();
        lRunSensor = false ;
        mSensorManager.unregisterListener(HomeScreen.this);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_screen);

        lastUpdate = System.currentTimeMillis();

        ss = new Intent(this,sensorService.class);
        final EditText ipAdr  = (EditText)findViewById(R.id.fldIpAdr) ;
        final EditText portNo = (EditText)findViewById(R.id.fldPortNo) ;

        btnStart = (Button)findViewById(R.id.btnStart) ;
        btnStop  = (Button)findViewById(R.id.btnStop) ;

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        accSensor      = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) ;

        final TextView LogTextView = (TextView)findViewById(R.id.cntLog);
        LogTextView.clearComposingText();
        LogTextView.append("Object Started.. Whoop step 1");

        btnStart.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                IP_ADDRESS = ipAdr.getText().toString();
                PORT_NUMBER = Integer.parseInt(portNo.getText().toString());
                mSensorManager.registerListener(HomeScreen.this, accSensor, SensorManager.SENSOR_DELAY_FASTEST) ;
                lRunSensor = true ;
                LogTextView.append("\nStart Button clicked...\nIP Address: " + IP_ADDRESS + ":" + PORT_NUMBER);
            }
        });

        btnStop.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                onPause();
                lRunSensor = false ;
                LogTextView.append("\nStuff should be closed and unregistered...");
            }
        });


    }

    @Override
    public void onSensorChanged(final SensorEvent event) {

        if(!lRunSensor) return;

        long actualTime ;
        actualTime = System.currentTimeMillis();

        if (actualTime - lastUpdate < 175) {
            return;
        }
        lastUpdate = actualTime;

        /*
        class Thread implements SensorEventListener {

            @Override
            public void onSensorChanged(SensorEvent event) {

            }

            @Override
            public void onAccuracyChanged(Sensor sensor, int accuracy) {

            }
        }
        */

        Thread newThread = new Thread(new Thread() {

            public void run(SensorEvent event){
                try {
                    oStream.writeBytes("x:" + event.values[0] + "," + "y:" + event.values[1] + "," + "z:" + event.values[2]);
                    oStream.flush();
                } catch (IOException e) {
                    return ;
                }
            }
            @Override
            public void run() {
                try {
                    dataSocket = new Socket(IP_ADDRESS, PORT_NUMBER);
                    oStream = new DataOutputStream(dataSocket.getOutputStream());
                    run(event);
                    oStream.close();
                    dataSocket.close();
                } catch (UnknownHostException e) {
                    return ;
                } catch (Exception e) {
                    return ;
                }
            }
        });
        newThread.start();
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

}
