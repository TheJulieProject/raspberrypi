package com.uom.pimote.managers;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.ProgressBar;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.ToggleButton;

import com.uom.pimote.Communicator;
import com.uom.pimote.R;
import com.uom.pimote.TCPClient;
import com.uom.pimote.mjpegvideo.MjpegView;

import java.util.ArrayList;

public class RegularButtonManager extends PimoteManager {

    private static final int SETUP = 1;
    private static final int REQUEST_OUTPUT_CHANGE = 2;
    private static final int BUTTON = 1, TEXT_INPUT = 2, TOGGLE_BUTTON = 3, TEXT_OUTPUT = 4,
                             VIDEO_FEED = 5, VOICE_INPUT = 6, RECURRING_INFO = 7, PROGRESS_BAR = 8;
    TCPClient tcp;
    Context c;
    LinearLayout layout;
    String ip;
    int viewPosition;

    public RegularButtonManager(Context c, TCPClient tcp, String ip, String name) {
        super(tcp);
        this.c = c;
        this.tcp = tcp;
        this.ip = ip;
        this.viewPosition = 0;
        ((Communicator) c).getActionBar().show();
        ((Communicator) c).getActionBar().setTitle(name);
        Log.d("TITLE", name);
        ((Communicator) c).setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        ((Communicator) c).setContentView(R.layout.activity_main);
        this.layout = (LinearLayout) ((Communicator) c).findViewById(R.id.mainlayout);
        threads = new ArrayList<RecurringInfo>();
    }

    @Override
    public void onMessage(String[] message) {
        switch (Integer.parseInt(message[0])) {
            case SETUP:
                String[] setup = new String[message.length - 1];
                for (int i = 1; i < message.length; i++)
                    setup[i - 1] = message[i];
                addButtons(setup);
                break;

            case REQUEST_OUTPUT_CHANGE:
                if (Integer.parseInt(message[1]) == TEXT_OUTPUT) {
                    TextView output = getTextView(Integer.parseInt(message[2]));
                    output.setText(message[3]);
                } else if (Integer.parseInt(message[1]) == PROGRESS_BAR) {
                    ProgressBar bar = getProgressBar(Integer.parseInt(message[2]));
                    bar.setProgress(Integer.parseInt(message[3]));
                }
                break;
        }
    }

    public void addButtons(final String[] setup) {
        switch (Integer.parseInt(setup[0])) {
            case BUTTON:
                addNewButton(setup);
                break;
            case TEXT_INPUT:
                addNewTextInput(setup);
                break;
            case TOGGLE_BUTTON:
                addNewToggle(setup);
                break;
            case TEXT_OUTPUT:
                addNewTextView(setup);
                break;
            case VIDEO_FEED:
                addNewFeed(setup, ip);
                break;
            case VOICE_INPUT:
                addVoiceInput(setup);
                break;
            case RECURRING_INFO:
                addRecurringInformation(Integer.parseInt(setup[1]), Integer.parseInt(setup[2]), tcp);
                break;
            case PROGRESS_BAR:
                addProgressBar(Integer.parseInt(setup[1]), Integer.parseInt(setup[2]));
            default:
                Log.e("SETUP", "Unknown component");
        }
    }

    public void addNewButton(final String[] setup) {
        Button button = new Button(c);
        button.setText(setup[2]);
        button.setOnClickListener(new OnClickListener() {
            public void onClick(View v) {
                if (tcp != null)
                    send(setup[1] + "," + " ");
            }
        });

        layout.addView(button, viewPosition++);
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
                if (tcp != null) {
                    String text = addText.getText().toString();
                    if (text.equals("")) text = "null";
                    send(setup[1] + "," + text);
                }
                addText.setText("");
            }
        });
        textButtonLayout.addView(addText);
        textButtonLayout.addView(button);
        layout.addView(textButtonLayout, viewPosition++);
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
                send(setup[1] + "," + tf);
            }
        });
        textButtonLayout.addView(text);
        textButtonLayout.addView(button);
        layout.addView(textButtonLayout, viewPosition++);
    }

    public void addNewTextView(final String[] setup) {
        LayoutParams params = new LayoutParams(LayoutParams.MATCH_PARENT,
                LayoutParams.WRAP_CONTENT);
        params.setMargins(0, 10, 0, 10);
        TextView text = new TextView(c);
        text.setTextSize(18);
        text.setLayoutParams(params);
        if (setup.length == 3)
            text.setText(setup[2]);
        layout.addView(text, viewPosition++);
        text.setId(Integer.parseInt(setup[1]));
    }

    public TextView getTextView(int id) {
        return (TextView) ((Communicator) c).findViewById(id);
    }
    public ProgressBar getProgressBar(int id){
        return (ProgressBar) ((Communicator)c).findViewById(id);
    }

    public void addNewFeed(String[] setup, String ip) {
        String feedIp = ip;
        if (Integer.parseInt(setup[3]) == 1) feedIp = setup[4];
        String URL = "http://" + feedIp + ":8080/?action=stream";
        MjpegView mv = (MjpegView) ((Communicator) c).findViewById(R.id.mv2);
        startVideo(mv, URL);
        LayoutParams params = new LayoutParams(Integer.parseInt(setup[1]), Integer.parseInt(setup[2]));
        params.setMargins(0, 10, 0, 10);
        mv.setLayoutParams(params);
        mv.setVisibility(View.VISIBLE);
        viewPosition++;
    }

    public void addVoiceInput(final String[] setup) {
        ImageButton voice = new ImageButton(c);
        voice.setImageDrawable(c.getResources().getDrawable(R.drawable.mic));
        LayoutParams params = new LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 100);
        voice.setScaleType(ImageView.ScaleType.CENTER_INSIDE);
        voice.setLayoutParams(params);
        final int id = Integer.parseInt(setup[1]);
        voice.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                ((Communicator) c).startVoiceRecognition(id);
            } // onClick()
        });
        layout.addView(voice, viewPosition++);
    }

    public void addProgressBar(int id, int maxValue){
        ProgressBar bar = new ProgressBar(c, null, android.R.attr.progressBarStyleHorizontal);
        bar.setProgress(0);
        bar.setMax(maxValue);
        bar.setId(id);
        layout.addView(bar);
    }


}
