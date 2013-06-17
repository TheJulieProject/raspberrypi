package com.uom.pimote;

import android.content.Context;
import android.os.Handler;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnTouchListener;
import android.widget.ImageView;
import android.widget.TextView;

public class ControllerManager {

	boolean running = true;
	boolean forwardPress, backPress, leftPress, rightPress = false;
	TCPClient tcp;

	Thread t;

	public ControllerManager(Context c, final TCPClient tcp, final int pollRate) {
		((Communicator) c).setContentView(R.layout.controllayout);
		this.tcp = tcp;
		final int sleepTime = 1000/pollRate;
		final ImageView forward;
		final ImageView backwards;
		final ImageView left;
		final ImageView right;
		final TextView debug;
		forward = (ImageView) ((Communicator) c)
				.findViewById(R.id.control_forward);
		backwards = (ImageView) ((Communicator) c)
				.findViewById(R.id.control_back);
		left = (ImageView) ((Communicator) c).findViewById(R.id.control_left);
		right = (ImageView) ((Communicator) c).findViewById(R.id.control_right);
		debug = (TextView) ((Communicator) c).findViewById(R.id.debugText);
		forward.setClickable(true);
		backwards.setClickable(true);
		left.setClickable(true);
		right.setClickable(true);

		forward.setOnTouchListener(new OnTouchListener() {

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
		backwards.setOnTouchListener(new OnTouchListener() {

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
		left.setOnTouchListener(new OnTouchListener() {

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
		right.setOnTouchListener(new OnTouchListener() {

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

		t.start();
	}

	public void toggleControl(int position, boolean value) {
		switch (position) {
		case 1:
			forwardPress = value;
			break;
		case 2:
			backPress = value;
			break;
		case 3:
			leftPress = value;
			break;
		case 4:
			rightPress = value;
			break;
		}
	}

	public void stop() {
		running = false;
	}
}
