package com.uom.pimote;

import android.app.Activity;
import android.content.Intent;
import android.content.pm.ActivityInfo;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.ArrayList;

public class Communicator extends Activity {


    private static final int NORMAL_CONTROL = 0;
    private static final int JOYSTICK_CONTROL = 1;
    private static final int REQUEST_CODE = 1234;
    private static int controlType = -1;
    TCPClient tcp;
    String ip;
    int port;
    AsyncTask<String, String, TCPClient> task = null;
    RegularButtonManager regular = null;
    ControllerManager cm = null;
    boolean setup = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //setContentView(R.layout.activity_main);

        try {
            Bundle b = getIntent().getExtras();
            port = b.getInt("port");
            ip = b.getString("ip");
        } catch (Exception e) {
            endActivity("Bad Arguments");
        }

        if (task == null)
            task = new connectTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, "");


    }

    /* Fire an intent to start the voice recognition activity. */
    public void startVoiceRecognition() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Voice recognition Demo...");
        startActivityForResult(intent, REQUEST_CODE);
    } // startRecording()

    /* Handle the results from the voice recognition activity. */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            // Populate the wordsList with the String values the recognition engine thought it heard
            ArrayList<String> matches = data.getStringArrayListExtra(
                    RecognizerIntent.EXTRA_RESULTS);
            tcp.sendMessage(matches.get(0));
        }
        super.onActivityResult(requestCode, resultCode, data);
    } // onActivityResult()

    @Override
    protected void onStop() {
        super.onStop();
        task.cancel(true);
        if (cm != null) cm.stopPlayback();
        if (regular != null) regular.stop();
        finish();
        Log.e("pi", "Ending");
        tcp.stopClient();
    }

    public void endActivity(String msg) {
        if (cm != null) cm.stopPlayback();
        if (regular != null) regular.stop();
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
                if (controlType == JOYSTICK_CONTROL) {
                    getActionBar().hide();
                    setContentView(R.layout.controllayout);
                    setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
                    cm = new ControllerManager(Communicator.this, tcp,
                            Integer.parseInt(info[1]), ip, Integer.parseInt(info[2]), Integer.parseInt(info[3]));
                } else {
                    getActionBar().show();
                    setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
                    setContentView(R.layout.activity_main);
                    LinearLayout layout = (LinearLayout) findViewById(R.id.mainlayout);
                    regular = new RegularButtonManager(Communicator.this, tcp,
                            layout);
                }
                setup = true;
            } else { //setup was done
                int type = Integer.parseInt(info[0]);
                String[] setup = new String[info.length - 1];
                for (int i = 1; i < info.length; i++) {
                    setup[i - 1] = info[i];
                }
                if (type == 0) {
                    if (controlType == NORMAL_CONTROL) {
                        regular.addButtons(setup);
                    }
                } else if (type == 1) { //request to change text on a textview
                    TextView output = regular.getTextView(Integer.parseInt(setup[0]));
                    output.setText(setup[1]);
                }

            }
        }
    }
}
