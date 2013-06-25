package com.uom.pimote;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.os.AsyncTask;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.ToggleButton;

import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;

public class RegularButtonManager {


    //TextView[] outputs;
    TCPClient tcp;
    Context c;
    LinearLayout layout;
    ArrayList<TextView> outputs;
    MjpegView mv = null;
    AsyncTask<String, Void, MjpegInputStream> read = null;

    public RegularButtonManager(Context c, TCPClient tcp, LinearLayout layout) {
        this.c = c;
        this.tcp = tcp;
        this.layout = layout;
        ((Communicator) c).setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        outputs = new ArrayList<TextView>();
    }

    public void addButtons(final String[] setup) {
        switch (Integer.parseInt(setup[0])) {
            case 1:
                addNewButton(setup);
                break;
            case 2:
                addNewTextInput(setup);
                break;
            case 3:
                addNewToggle(setup);
                break;
            case 4:
                addNewTextView(setup);
                break;
            case 5:
                addNewFeed(setup);
                break;
        }
    }

    public void addNewButton(final String[] setup) {
        Button button = new Button(c);
        button.setText(setup[2]);
        button.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
                if (tcp != null)
                    tcp.sendMessage(setup[1] + "," + " ");
            }
        });

        layout.addView(button);
    }

    public void addNewTextInput(final String[] setup) {
        LinearLayout textButtonLayout = new LinearLayout(c);
        LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 10, 0, 10);
        textButtonLayout.setLayoutParams(params);
        final EditText addText = new EditText(c);
        addText.setHint(setup[2]);
        LayoutParams params2 = new TableRow.LayoutParams(0,
                LayoutParams.WRAP_CONTENT, 1f);
        addText.setLayoutParams(params2);
        Button button = new Button(c);
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

    public void addNewToggle(final String[] setup) {
        LinearLayout textButtonLayout = new LinearLayout(c);
        LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 10, 0, 10);
        textButtonLayout.setLayoutParams(params);
        TextView text = new TextView(c);
        text.setTextSize(18);
        text.setText(setup[2]);
        LayoutParams params2 = new TableRow.LayoutParams(0,
                LayoutParams.WRAP_CONTENT, 1f);
        text.setLayoutParams(params2);
        ToggleButton button = new ToggleButton(c);
        boolean checked = Integer.parseInt(setup[3]) == 1;
        button.setChecked(checked);
        button.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View view) {
                int tf = ((ToggleButton) view).isChecked() ? 1 : 0;
                tcp.sendMessage(setup[1] + "," + tf);
            }
        });
        textButtonLayout.addView(text);
        textButtonLayout.addView(button);
        layout.addView(textButtonLayout);
    }

    public void addNewTextView(final String[] setup) {
        LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 10, 0, 10);
        TextView text = new TextView(c);
        text.setTextSize(18);
        text.setLayoutParams(params);
        if(setup.length == 3)
        text.setText(setup[2]);
        layout.addView(text);
        outputs.add(text);
    }

    public TextView getTextView(int id) {
        return outputs.get(id);
    }

    public void addNewFeed(String[] setup) {
        Log.e("MJPG", setup[1]);
        String URL = "http://" + setup[1] + ":8080/?action=stream";
        mv = (MjpegView)((Communicator)c).findViewById(R.id.mv2);
        read = new DoRead().executeOnExecutor(AsyncTask.THREAD_POOL_EXECUTOR, URL);
        LayoutParams params = new LayoutParams(Integer.parseInt(setup[2]),Integer.parseInt(setup[3]));
        params.setMargins(0,10,0,10);
        mv.setLayoutParams(params);
        mv.setVisibility(View.VISIBLE);
        Log.e("MJPG", mv.getMeasuredWidth() + "," + mv.getMeasuredHeight());
    }

    public void stop() {
        if (mv != null) {
            mv.stopPlayback();
            read.cancel(true);
        }
    }

    public class DoRead extends AsyncTask<String, Void, MjpegInputStream> {
        protected MjpegInputStream doInBackground(String... url) {
            //TODO: if camera has authentication deal with it and don't just not work
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
}
