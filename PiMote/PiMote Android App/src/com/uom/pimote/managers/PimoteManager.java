package com.uom.pimote.managers;

import android.os.AsyncTask;
import android.util.Log;

import com.uom.pimote.Communicator;
import com.uom.pimote.TCPClient;
import com.uom.pimote.mjpegvideo.MjpegInputStream;
import com.uom.pimote.mjpegvideo.MjpegView;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;

/**
 * Created by Tom on 02/07/2013.
 */
public class PimoteManager {
    MjpegView mv = null;
    AsyncTask<String, Void, MjpegInputStream> read = null;
    ArrayList<RecurringInfo> threads;
    TCPClient tcp;

    public PimoteManager(TCPClient tcp) {
        this.tcp = tcp;
        threads = new ArrayList<RecurringInfo>();
    }

    public void onMessage(String[] message) {
    }

    ;

    public void startVideo(MjpegView mv, String URL) {
        this.mv = mv;
        read = new DoRead().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, URL);
    }

    public void stopVideo() {
        if (mv != null) {
            read.cancel(true);
            mv.stopPlayback();
        }
    }

    public void pauseVideo() {
        if (mv != null) mv.pause();
    }

    public void resumeVideo() {
        if (mv != null) mv.resume();
    }

    public void addRecurringInformation(final String[] setup, TCPClient tcp) {
        RecurringInfo t = new RecurringInfo(setup, tcp);
        threads.add(t);
        t.start();
    }

    public void stopAllThreads() {
        for (int i = 0; i < threads.size(); i++) {
            threads.get(i).stopThread();
        }
        stopVideo();
    }

    public class DoRead extends AsyncTask<String, Void, MjpegInputStream> {
        protected MjpegInputStream doInBackground(String... url) {
            HttpResponse res = null;
            DefaultHttpClient httpclient = new DefaultHttpClient();
            Log.d("MjpegRegular", "1. Sending http request");
            try {
                res = httpclient.execute(new HttpGet(URI.create(url[0])));
                Log.d("MjpegRegular", "2. Request finished, status = " + res.getStatusLine().getStatusCode());
                if (res.getStatusLine().getStatusCode() == 401) {
                    //You must turn off camera User Access Control before this will work
                    return null;
                }
                return new MjpegInputStream(res.getEntity().getContent());
            } catch (ClientProtocolException e) {
                e.printStackTrace();
                Log.d("MjpegRegular", "Request failed-ClientProtocolException", e);
                //Error connecting to camera
            } catch (IOException e) {
                e.printStackTrace();
                Log.d("MjpegRegular", "Request failed-IOException", e);
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

    public void send(String message){
        tcp.sendMessage(Communicator.SEND_DATA + "," + message);
    }

    class RecurringInfo extends Thread {
        boolean running = true;
        String id;
        int sleepTime;
        TCPClient tcp;

        public RecurringInfo(String[] setup, TCPClient tcp) {
            id = setup[1];
            sleepTime = Integer.parseInt(setup[2]);
            this.tcp = tcp;
        }

        @Override
        public void run() {
            while (running) {
                try {
                    tcp.sendMessage(Communicator.SEND_DATA + "," + id);
                    Thread.sleep(sleepTime);
                } catch (Exception e) {
                    Log.e("THREAD", "Sleep error");
                }
            }
        }

        public void stopThread() {
            running = false;
        }
    }

}
