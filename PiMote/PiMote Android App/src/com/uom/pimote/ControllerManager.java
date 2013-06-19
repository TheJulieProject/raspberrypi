package com.uom.pimote;

import android.content.Context;
import android.os.Handler;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.ImageView;
import android.widget.TextView;
import android.content.pm.ActivityInfo;

public class ControllerManager {

    boolean running = true;
    boolean forwardPress, backPress, leftPress, rightPress = false;
    TCPClient tcp;
    
    Thread t;

    public ControllerManager(Context c, final TCPClient tcp, final int pollRate) {
        ((Communicator) c).setContentView(R.layout.controllayout);
        ((Communicator) c).setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE);
        this.tcp = tcp;
        final int sleepTime = 1000 / pollRate;
        final ImageView leftForward;
        final ImageView leftBackwards;
        final ImageView rightForward;
        final ImageView rightBackwards;
        final TextView debug;

        leftForward = (ImageView) ((Communicator) c).findViewById(R.id.left_motor_forward);
        leftBackwards = (ImageView) ((Communicator) c).findViewById(R.id.left_motor_backwards);
        rightForward = (ImageView) ((Communicator) c).findViewById(R.id.right_motor_forward);
        rightBackwards = (ImageView) ((Communicator) c).findViewById(R.id.right_motor_backwards);
        debug = (TextView) ((Communicator) c).findViewById(R.id.debugText);

        leftForward.setClickable(true);
        leftBackwards.setClickable(true);
        rightForward.setClickable(true);
        rightBackwards.setClickable(true);

        leftForward.setOnTouchListener(new OnTouchListener() {

            @Override
            public boolean onTouch(View v, MotionEvent event) {
                // TODO Auto-generated method stub
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
                // TODO Auto-generated method stub
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
                // TODO Auto-generated method stub
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
                // TODO Auto-generated method stub
                if (event.getAction() == MotionEvent.ACTION_DOWN
                        || event.getAction() == MotionEvent.ACTION_UP)
                    toggleControl(4,
                            event.getAction() == MotionEvent.ACTION_DOWN);
                return false;
            }

        });

        final Handler handler = new Handler();
        t = new Thread() {
            public void run() {
                while (running) {
                    handler.post(new Runnable() {
                        public void run() {
                            debug.setText("DEBUG\n\nPoll Rate: " + pollRate + "/s\nF: " + forwardPress
                                    + "\nB: " + backPress + "\nL: " + leftPress
                                    + "\nR: " + rightPress);
                        }
                    });
                    if (forwardPress) {
                        if (rightPress) {
                            tcp.sendMessage("2");
                        } else if (leftPress) {
                            tcp.sendMessage("1");
                        } else {
                            tcp.sendMessage("0");
                        }
                    } else if (backPress) {
                        if (rightPress) {
                            tcp.sendMessage("5");
                        } else if (leftPress) {
                            tcp.sendMessage("4");
                        } else {
                            tcp.sendMessage("3");
                        }
                    } else if (rightPress) {
                        tcp.sendMessage("6");
                    } else if (leftPress) {
                        tcp.sendMessage("7");
                    }

                    try {
                        sleep(sleepTime);
                    } catch (Exception e) {
                    }
                }
            }
        };

        //t.start();
    }

    public void toggleControl(int position, boolean value) {
        int flag = value ? 1 : 0;
        switch (position) {
            case 1:
                if (forwardPress != value)
                    tcp.sendMessage("" + (0 + flag));
                forwardPress = value;
                break;
            case 2:
                if (backPress != value)
                    tcp.sendMessage("" + (2 + flag));
                backPress = value;
                break;
            case 3:
                if (leftPress != value)
                    tcp.sendMessage("" + (4 + flag));
                leftPress = value;
                break;
            case 4:
                if (rightPress != value)
                    tcp.sendMessage("" + (6 + flag));
                rightPress = value;
                break;
        }
    }

    public void stop() {
        running = false;
    }
}
