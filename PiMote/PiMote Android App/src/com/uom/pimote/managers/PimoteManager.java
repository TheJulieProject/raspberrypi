package com.uom.pimote.managers;

import android.util.Log;

import com.uom.pimote.Communicator;
import com.uom.pimote.TCPClient;
import com.uom.pimote.mjpegvideo.MjpegStreamManager;
import com.uom.pimote.mjpegvideo.MjpegView;

import java.util.ArrayList;

/**
 * Created by Tom on 02/07/2013.
 */
public class PimoteManager {
    ArrayList<RecurringInfo> threads;
    TCPClient tcp;
    ArrayList<MjpegStreamManager> streams;

    public PimoteManager(TCPClient tcp) {
        this.tcp = tcp;
        threads = new ArrayList<RecurringInfo>();
        streams = new ArrayList<MjpegStreamManager>();
    }

    public void onMessage(String[] message) {
    }

    public void startVideo(MjpegView mv, String URL) {
        MjpegStreamManager stream = new MjpegStreamManager();
        streams.add(stream);
        stream.startVideo(mv, URL);
    }

    public void stopVideo() {
        for(MjpegStreamManager s : streams){
            s.stopVideo();
        }
    }

    public void pauseVideo() {
        for(MjpegStreamManager s : streams){
            s.pauseVideo();
        }
    }

    public void resumeVideo() {
        for(MjpegStreamManager s : streams){
            s.resumeVideo();
        }
    }

    public void addRecurringInformation(int id, int sleepTime, TCPClient tcp) {
        RecurringInfo t = new RecurringInfo(id, sleepTime, tcp);
        threads.add(t);
        t.start();
    }

    public void stopAllThreads() {
        for (int i = 0; i < threads.size(); i++) {
            threads.get(i).stopThread();
        }
        stopVideo();
    }



    public void send(String message){
        tcp.sendMessage(Communicator.SEND_DATA + "," + message);
    }

    class RecurringInfo extends Thread {
        boolean running = true;
        int id;
        int sleepTime;
        TCPClient tcp;

        public RecurringInfo(int id, int sleepTime, TCPClient tcp) {
            this.tcp = tcp;
            this.id = id;
            this.sleepTime = sleepTime;
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
