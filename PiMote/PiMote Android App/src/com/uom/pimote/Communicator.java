package com.uom.pimote;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.widget.LinearLayout;
import android.widget.TextView;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.params.HttpConnectionParams;
import org.apache.http.params.HttpParams;

import java.io.IOException;
import java.net.URI;

public class Communicator extends Activity {


    private static final int NORMAL_CONTROL = 0;
    private static final int JOYSTICK_CONTROL = 1;
    private static int controlType = -1;
    TCPClient tcp;
    String ip;
    int port;
    LinearLayout layout;
    AsyncTask<String, String, TCPClient> task;
    RegularButtonManager regular = null;
    ControllerManager cm = null;
    boolean setup = false;

    // Mjpeg streamer variables
    private static final String TAG = "MJPEG";
    private MjpegView mv = null;
    String URL;
    private static final int REQUEST_SETTINGS = 0;
    private int width = 320;
    private int height = 240;
    private boolean suspending = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        try {
            Bundle b = getIntent().getExtras();
            port = b.getInt("port");
            ip = b.getString("ip");

            URL = new String("http://" + ip + ":8080/?action=stream");
        } catch (Exception e) {
            endActivity("Bad Arguments");
        }
        layout = (LinearLayout) findViewById(R.id.mainlayout);
        task = new connectTask().execute("");

        mv = (MjpegView) findViewById(R.id.mv);
        if(mv != null)
            mv.setResolution(width, height);
        new DoRead().execute(URL);
    }

    public class DoRead extends AsyncTask<String, Void, MjpegInputStream> {
        protected MjpegInputStream doInBackground(String... url) {
            //TODO: if camera has authentication deal with it and don't just not work
            HttpResponse res = null;
            DefaultHttpClient httpclient = new DefaultHttpClient();
            HttpParams httpParams = httpclient.getParams();
            HttpConnectionParams.setConnectionTimeout(httpParams, 5 * 1000);
            Log.d(TAG, "1. Sending http request");
            try {
                res = httpclient.execute(new HttpGet(URI.create(url[0])));
                Log.d(TAG, "2. Request finished, status = " + res.getStatusLine().getStatusCode());
                if(res.getStatusLine().getStatusCode()==401){
                    //You must turn off camera User Access Control before this will work
                    return null;
                }
                return new MjpegInputStream(res.getEntity().getContent());
            } catch (ClientProtocolException e) {
                e.printStackTrace();
                Log.d(TAG, "Request failed-ClientProtocolException", e);
                //Error connecting to camera
            } catch (IOException e) {
                e.printStackTrace();
                Log.d(TAG, "Request failed-IOException", e);
                //Error connecting to camera
            }
            return null;
        }

        protected void onPostExecute(MjpegInputStream result) {
            mv.setSource(result);
            if(result!=null) result.setSkip(1);
            mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
            mv.showFps(false);
        }
    }

    @Override
    protected void onPause() {
        super.onPause();
        finish();
    }

    @Override
    protected void onStop() {
        super.onStop();
        Log.d("pi", "Ending");
        tcp.stopClient();
        task.cancel(true);
    }

    public void endActivity(String msg) {
        Intent i = new Intent(this, Main.class);
        Bundle b = new Bundle();
        b.putString("pr", msg);
        i.putExtras(b);
        startActivity(i);
        finish();
    }

    @Override
    public void onBackPressed() {
        endActivity("");
    }

    public class connectTask extends AsyncTask<String, String, TCPClient> {

        @Override
        protected TCPClient doInBackground(String... message) {

            // we create a TCPClient object and
            tcp = new TCPClient(new TCPClient.OnMessageReceived() {
                @Override
                // here the messageReceived method is implemented
                public void messageReceived(String message) {
                    // this method calls the onProgressUpdate
                    publishProgress(message);
                }

                public void failActivity(String msg) {
                    endActivity(msg);
                }
            }, ip, port);
            tcp.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            final String[] info = values[0].split(",");
            // Log.d("pi", info[0] + ", " + info[1]);

            if (!setup) {
                Log.e("TCPClient", "Setting up");
                controlType = Integer.parseInt(info[0]);
                if (controlType == JOYSTICK_CONTROL)
                    cm = new ControllerManager(Communicator.this, tcp,
                            Integer.parseInt(info[1]));
                else
                    regular = new RegularButtonManager(Communicator.this, tcp,
                            layout);
                setup = true;
            } else {
                int type = Integer.parseInt(info[0]);
                String[] setup = new String[info.length-1];
                for(int i = 1; i < info.length; i++){
                    setup[i-1] = info[i];
                }
                if (type== 0) {
                    if (controlType == NORMAL_CONTROL) {

                        regular.addButtons(setup);
                    }
                }else if(type== 1){ //request to change text on a textview
                    Log.e("TCPClient", "Text is to be changed to: " + setup[1]);
                    TextView output = regular.getTextView(Integer.parseInt(setup[0]));
                    output.setText(setup[1]);
                }

            }
        }
    }
}
