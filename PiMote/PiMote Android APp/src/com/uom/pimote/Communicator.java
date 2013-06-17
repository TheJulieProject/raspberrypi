package com.uom.pimote;

import android.app.Activity;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnTouchListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.TableRow;
import android.widget.TextView;

public class Communicator extends Activity {

	TCPClient tcp;

	String ip;
	int port;
	LinearLayout layout;

	private static final int NORMAL_CONTROL = 0;
	private static final int JOYSTICK_CONTROL = 1;

	AsyncTask<String, String, TCPClient> task;

	Thread t = null;

	boolean running = true;

	boolean forwardPress, backPress, leftPress, rightPress = false;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		try {
			Bundle b = getIntent().getExtras();
			port = b.getInt("port");
			ip = b.getString("ip");
		} catch (Exception e) {
			endActivity("Bad Arguments");
		}
		layout = (LinearLayout) findViewById(R.id.mainlayout);
		task = new connectTask().execute("");
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
			switch (Integer.parseInt(info[0])) {
			case NORMAL_CONTROL:
				String[] setup = new String[info.length - 1];
				for (int i = 1; i < info.length; i++)
					setup[i - 1] = info[i];
				addButtons(setup);
				break;
			case JOYSTICK_CONTROL:
				setUpController();
			}
			// button.setOnTouchListener(new RepeatListener(100, 100, new
			// OnClickListener() {
			// @Override
			// public void onClick(View view) {
			// the code to execute repeatedly
			// if(tcp!=null)
			// tcp.sendMessage(info[0]);
			// }
			// }));

			// output.append("\nPi: "+values[0]);
		}
	}

	public void setUpController() {
		this.setContentView(R.layout.controllayout);

		final ImageView forward;
		final ImageView backwards;
		final ImageView left;
		final ImageView right;
		final TextView debug;
		forward = (ImageView) findViewById(R.id.control_forward);
		backwards = (ImageView) findViewById(R.id.control_back);
		left = (ImageView) findViewById(R.id.control_left);
		right = (ImageView) findViewById(R.id.control_right);
		debug = (TextView) findViewById(R.id.debugText);
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
				toggleControl(1, event.getAction() == MotionEvent.ACTION_DOWN);
				return false;
			}

		});
		backwards.setOnTouchListener(new OnTouchListener() {

			@Override
			public boolean onTouch(View v, MotionEvent event) {
				// TODO Auto-generated method stub
				if (event.getAction() == MotionEvent.ACTION_DOWN
						|| event.getAction() == MotionEvent.ACTION_UP)
				toggleControl(2, event.getAction() == MotionEvent.ACTION_DOWN);
				return false;
			}

		});
		left.setOnTouchListener(new OnTouchListener() {

			@Override
			public boolean onTouch(View v, MotionEvent event) {
				// TODO Auto-generated method stub
				if (event.getAction() == MotionEvent.ACTION_DOWN
						|| event.getAction() == MotionEvent.ACTION_UP)
				toggleControl(3, event.getAction() == MotionEvent.ACTION_DOWN);
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
					//handler.post(new Runnable(){
	                    //public void run() {debug.setText("DEBUG\n\nF: " + forwardPress + "\nB: "+ backPress + "\nL: " + leftPress  + "\nR: " + rightPress);}});
					// Log.d("Pi", "Check");
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
						sleep(100);
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

	public void addButtons(final String[] setup) {
		if (Integer.parseInt(setup[0]) == 1) {
			Button button = new Button(Communicator.this);
			button.setText(setup[2]);
			button.setOnClickListener(new OnClickListener() {
				public void onClick(View v) {
					if (tcp != null)
						tcp.sendMessage(setup[1] + "," + " ");
				}
			});
			layout.addView(button);
		} else if (Integer.parseInt(setup[0]) == 2) {
			LinearLayout textButtonLayout = new LinearLayout(Communicator.this);
			LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
					LayoutParams.WRAP_CONTENT);
			textButtonLayout.setLayoutParams(params);
			final EditText addText = new EditText(Communicator.this);
			addText.setHint(setup[2]);
			LayoutParams params2 = new TableRow.LayoutParams(0,
					LayoutParams.WRAP_CONTENT, 1f);
			addText.setLayoutParams(params2);
			Button button = new Button(Communicator.this);
			button.setText("Send");
			button.setGravity(3);
			button.setOnClickListener(new OnClickListener() {
				public void onClick(View v) {
					if (tcp != null)
						tcp.sendMessage(setup[1] + ","
								+ addText.getText().toString());
					addText.setText("");
				}
			});
			textButtonLayout.addView(addText);
			textButtonLayout.addView(button);
			layout.addView(textButtonLayout);
		}
	}

	protected void onPause() {
		super.onPause();
		running = false;
		finish();
	}

	@Override
	protected void onStop() {
		super.onStop();
		Log.d("pi", "Ending");
		tcp.stopClient();
		running = false;
		task.cancel(true);
	}

	public void endActivity(String msg) {
		Intent i = new Intent(this, Main.class);
		Bundle b = new Bundle();
		b.putString("pr", msg);
		i.putExtras(b);
		running = false;
		startActivity(i);
		finish();
	}

	@Override
	public void onBackPressed() {
		endActivity("");
	}
}
