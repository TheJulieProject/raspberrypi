package com.uom.pimote;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.os.AsyncTask;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.ImageView;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.IOException;
import java.net.URI;

public class ControllerManager {

    // Mjpeg streamer variables
    private static final String TAG = "MJPEG";
    boolean forwardPress, backPress, leftPress, rightPress = false;
    TCPClient tcp;
    String URL;
    AsyncTask<String, Void, MjpegInputStream> read = null;
    ImageView hud;
    private MjpegView mv = null;

    public ControllerManager(final Context c, final TCPClient tcp, String ip, int videoV, int voiceV) {
        ((Communicator)c).getActionBar().hide();
        ((Communicator)c).setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        ((Communicator)c).setContentView(R.layout.controllayout);


        this.tcp = tcp;
        final ImageView leftForward;
        final ImageView leftBackwards;
        final ImageView rightForward;
        final ImageView rightBackwards;
        final ImageView microphone;



        boolean video = videoV != 0;
        boolean voice = voiceV != 0;
        leftForward = (ImageView) ((Communicator) c).findViewById(R.id.left_motor_forward);
        leftBackwards = (ImageView) ((Communicator) c).findViewById(R.id.left_motor_backwards);
        rightForward = (ImageView) ((Communicator) c).findViewById(R.id.right_motor_forward);
        rightBackwards = (ImageView) ((Communicator) c).findViewById(R.id.right_motor_backwards);
        microphone = (ImageView) ((Communicator) c).findViewById(R.id.microphone);
        hud = (ImageView) ((Communicator) c).findViewById(R.id.HUD);

        leftForward.setClickable(true);
        leftBackwards.setClickable(true);
        rightForward.setClickable(true);
        rightBackwards.setClickable(true);
        microphone.setClickable(true);

        leftForward.setOnTouchListener(new OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN
                        || event.getAction() == MotionEvent.ACTION_UP)
                    toggleControl(1,
                            event.getAction() == MotionEvent.ACTION_DOWN);
                return false;
            }

        });
        leftBackwards.setOnTouchListener(new OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN
                        || event.getAction() == MotionEvent.ACTION_UP)
                    toggleControl(2,
                            event.getAction() == MotionEvent.ACTION_DOWN);
                return false;
            }

        });
        rightForward.setOnTouchListener(new OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN
                        || event.getAction() == MotionEvent.ACTION_UP)
                    toggleControl(3,
                            event.getAction() == MotionEvent.ACTION_DOWN);
                return false;
            }

        });
        rightBackwards.setOnTouchListener(new OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                if (event.getAction() == MotionEvent.ACTION_DOWN
                        || event.getAction() == MotionEvent.ACTION_UP)
                    toggleControl(4,
                            event.getAction() == MotionEvent.ACTION_DOWN);
                return false;
            }

        });

        if (voice) {
            microphone.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View view) {
                    ((Communicator) c).startVoiceRecognition(1);
                } // onClick()
            });
            microphone.setVisibility(View.VISIBLE);
        } else {
            microphone.setVisibility(View.INVISIBLE);
        } // if - else

        URL = "http://" + ip + ":8080/?action=stream";

        mv = (MjpegView) ((Communicator) c).findViewById(R.id.mv);

        if (video) {
            mv.setVisibility(View.VISIBLE);
            hud.setVisibility(View.VISIBLE);
            read = new DoRead().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, URL);
        } else {
            mv.setVisibility(View.INVISIBLE);
            hud.setVisibility(View.INVISIBLE);
        }

    }

    public void stopPlayback() {
        if (read != null) {
            mv.stopPlayback();
            read.cancel(true);
        }
    }

    public void pause() {
        mv.pause();
    }

    public void resume() {
        mv.resume();
    }

    public void toggleControl(int position, boolean value) {
        int flag = value ? 1 : 0;
        switch (position) {
            case 1:
                if (forwardPress != value)
                    tcp.sendMessage(Communicator.SEND_DATA+","+"0," + (0 + flag));
                forwardPress = value;
                break;
            case 2:
                if (backPress != value)
                    tcp.sendMessage(Communicator.SEND_DATA+","+"0," + (2 + flag));
                backPress = value;
                break;
            case 3:
                if (leftPress != value)
                    tcp.sendMessage(Communicator.SEND_DATA+","+"0," + (4 + flag));
                leftPress = value;
                break;
            case 4:
                if (rightPress != value)
                    tcp.sendMessage(Communicator.SEND_DATA+","+"0," + (6 + flag));
                rightPress = value;
                break;
        }
    }

    public class DoRead extends AsyncTask<String, Void, MjpegInputStream> {
        protected MjpegInputStream doInBackground(String... url) {
            HttpResponse res = null;
            DefaultHttpClient httpclient = new DefaultHttpClient();
            Log.d(TAG, "1. Sending http request");
            try {
                res = httpclient.execute(new HttpGet(URI.create(url[0])));
                Log.d(TAG, "2. Request finished, status = " + res.getStatusLine().getStatusCode());
                if (res.getStatusLine().getStatusCode() == 401) {
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
            mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
            mv.showFps(true);
        }
    }
}
