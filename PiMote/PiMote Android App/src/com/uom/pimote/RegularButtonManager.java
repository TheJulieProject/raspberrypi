package com.uom.pimote;

import android.content.Context;
import android.content.pm.ActivityInfo;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.LinearLayout.LayoutParams;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.ToggleButton;
import android.util.Log;
import java.util.ArrayList;

public class RegularButtonManager {


    //TextView[] outputs;
    TCPClient tcp;
    Context c;
    LinearLayout layout;
    ArrayList<TextView> outputs;

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
                Log.e("TCPClient", "Setup");
                break;
            case 2:
                addNewTextInput(setup);
                break;
            case 3:
                addNewToggle(setup);
                break;
            case 4: addNewTextView(setup);
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
        textButtonLayout.setLayoutParams(params);
        TextView text = new TextView(c);
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
        TextView text = new TextView(c);
        text.setLayoutParams(params);
        text.setText(setup[2]);
        layout.addView(text);
        outputs.add(text);
    }

    public TextView getTextView(int id){
        return outputs.get(id);
    }
}
