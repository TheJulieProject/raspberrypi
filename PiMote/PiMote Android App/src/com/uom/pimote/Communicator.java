package com.uom.pimote;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.AsyncTask;
import android.os.Bundle;
import android.speech.RecognizerIntent;
import android.util.Log;
import android.widget.EditText;

import com.uom.pimote.managers.ControllerManager;
import com.uom.pimote.managers.PimoteManager;
import com.uom.pimote.managers.RegularButtonManager;

import java.util.ArrayList;

public class Communicator extends Activity {


    public static final int SEND_PASSWORD = 0;
    public static final int SEND_DATA = 1;
    private static final int NORMAL_CONTROL = 0;
    private static final int JOYSTICK_CONTROL = 1;
    private static final int REQUEST_CODE = 1234;
    private static final int SET_CONTROL_TYPE = 0;
    private static final int REQUEST_PASSWORD = 9855;
    private static final int STORE_KEY = 5649;
    private static final int PASSWORD_FAIL = 2314;
    private static final int DISCONNECTED_BY_SERVER = 6234;
    private static final int MESSAGE_FOR_MANAGER = 7335;
    private static int controlType = -1;
    TCPClient tcp;
    String ip;
    int port;
    AsyncTask<String, String, TCPClient> task = null;
    PimoteManager manager = null;
    private boolean authTypeKey = false;
    private int lastvoicepress = -1;
    private boolean voiceRecognition = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        try {
            Bundle b = getIntent().getExtras();
            port = b.getInt("port");
            ip = b.getString("ip");
        } catch (Exception e) {
            endActivity("Bad Arguments", true);
        }

        if (task == null)
            task = new connectTask().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, "");
    }

    /* Fire an intent to start the voice recognition activity. */
    public void startVoiceRecognition(int id) {
        lastvoicepress = id;
        voiceRecognition = true;
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT, "Voice recognition Demo...");
        intent.putExtra("theid", id);
        startActivityForResult(intent, REQUEST_CODE);
    } // startRecording()

    /* Handle the results from the voice recognition activity. */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_CODE && resultCode == RESULT_OK) {
            // Populate the wordsList with the String values the recognition engine thought it heard
            ArrayList<String> matches = data.getStringArrayListExtra(
                    RecognizerIntent.EXTRA_RESULTS);
            try {
                tcp.sendMessage(Communicator.SEND_DATA + "," + lastvoicepress + "," + matches.get(0));
            } catch (NullPointerException e) {
                Log.e("VOICE", "No matches found");
            }
        }
        voiceRecognition = false;
        super.onActivityResult(requestCode, resultCode, data);
    } // onActivityResult()

    @Override
    protected void onStop() {
        super.onStop();
        endActivity("", false);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (!voiceRecognition) endActivity("", false);
        else {
            if (manager != null) manager.pauseVideo();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (manager != null) manager.resumeVideo();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
    }

    public void endActivity(String msg, boolean main) {
        if (manager != null) manager.stopAllThreads();
        tcp.stopClient();
        if (main) {
            Intent i = new Intent(this, Main.class);
            Bundle b = new Bundle();
            b.putString("pr", msg);
            i.putExtras(b);
            startActivity(i);
        }
        finish();
    }

    @Override
    public void onBackPressed() {
        endActivity("", true);
    }

    public void passwordDialog() {
        //new dialog
        AlertDialog.Builder alert = new AlertDialog.Builder(Communicator.this);

        alert.setTitle("Password");
        alert.setMessage("Input Server Password");

        final EditText input = new EditText(Communicator.this);
        alert.setView(input);

        alert.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                String password = input.getText().toString();
                tcp.sendMessage(SEND_PASSWORD + "," + password);
            }
        });

        alert.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int whichButton) {
                endActivity("Cancelled", true);
            }
        });
        alert.show();
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
                    endActivity(msg, true);
                }
            }, ip, port);
            tcp.run();

            return null;
        }

        @Override
        protected void onProgressUpdate(String... values) {
            super.onProgressUpdate(values);
            final String[] info = values[0].split(",");
            Log.d("pi", info[0]);

            switch (Integer.parseInt(info[0])) {
                case REQUEST_PASSWORD: {
                    SharedPreferences prefs = getSharedPreferences("pimotePrefs", MODE_PRIVATE);
                    if (prefs.contains(ip)) {
                        Log.e("SETUP", "Key used");
                        tcp.sendMessage(SEND_PASSWORD + "," + prefs.getString(ip, "lolfail"));
                        authTypeKey = true;
                    } else {
                        Log.e("SETUP", "Need password");
                        passwordDialog();
                    }
                }
                break;
                case STORE_KEY: {
                    Log.e("SETUP", "Storing password");
                    SharedPreferences prefs = getSharedPreferences("pimotePrefs", MODE_PRIVATE);
                    SharedPreferences.Editor edit = prefs.edit();
                    edit.putString(ip, info[1]);
                    edit.commit();
                }
                break;
                case PASSWORD_FAIL:
                    if (authTypeKey) {
                        Log.e("SETUP", "Key fail");
                        SharedPreferences prefs = getSharedPreferences("pimotePrefs", MODE_PRIVATE);
                        SharedPreferences.Editor edit = prefs.edit();
                        edit.remove(ip);
                        passwordDialog();
                        authTypeKey = false;
                    } else {
                        Log.e("SETUP", "Password fail");
                        endActivity("Wrong Password", true);
                    }
                    break;

                case DISCONNECTED_BY_SERVER:
                    endActivity("Disconnected by server", true);
                    break;

                case SET_CONTROL_TYPE:
                    controlType = Integer.parseInt(info[1]);
                    if (controlType == NORMAL_CONTROL) {
                        manager = new RegularButtonManager(Communicator.this, tcp, ip, info[2], Integer.parseInt(info[3]));
                    } else if (controlType == JOYSTICK_CONTROL) {
                        manager = new ControllerManager(Communicator.this, tcp, ip,
                                Integer.parseInt(info[2]), Integer.parseInt(info[3]),
                                Integer.parseInt(info[4]), Integer.parseInt(info[5]));
                    }
                    break;

                case MESSAGE_FOR_MANAGER:
                    String[] message = new String[info.length - 1];
                    for (int i = 1; i < info.length; i++)
                        message[i - 1] = info[i];
                    manager.onMessage(message);
                    break;

                default:
                    Log.e("ERROR", "Wut?!");
                    break;
            }
        }
    }
}
