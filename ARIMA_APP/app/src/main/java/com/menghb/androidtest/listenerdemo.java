package com.menghb.androidtest;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.StrictMode;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.lang.ref.WeakReference;
import java.lang.reflect.Type;
import java.net.URL;
import java.net.URLConnection;

public class listenerdemo extends AppCompatActivity {
    private TextView main_vw;
    private final My_handler myhandler = new My_handler(this);
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.mainview);
//
//        if (android.os.Build.VERSION.SDK_INT > 9) {
//            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
//            StrictMode.setThreadPolicy(policy);}
        main_vw = findViewById(R.id.result);
        Button main_bt = findViewById(R.id.main_bt);
        main_bt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                My_thread m=new My_thread();
                m.setNum(1);
                new Thread(m).start();
            }
        });
        Button main_bt2=findViewById(R.id.main_bt2);
        main_bt2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                My_thread m=new My_thread();
                m.setNum(2);
                new Thread(m).start();
            }
        });
        Button main_bt3=findViewById(R.id.main_bt3);
        final EditText num_et = findViewById(R.id.edit_num);
        main_bt3.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final int num = Integer.valueOf(num_et.getText().toString());
                My_thread m=new My_thread();
                m.setNum(num);
                new Thread(m).start();
            }
        });

    }
    public class My_thread implements Runnable{
        private int day_num;
        public void setNum(int num)
        {
            this.day_num = num;
        }
        public void run() {
            StringBuilder json = new StringBuilder();
            try {
                String url = "http://192.168.31.235:8000/forecast/"+String.valueOf(day_num);
                URL urlobj = new URL(url);
                URLConnection connobj = urlobj.openConnection();
                //BufferedReader缓冲方式文本读取
                //InputStreamReader是字节流与字符流之间的桥梁，能将字节流输出为字符流，
                //并且能为字节流指定字符集，可输出一个个的字符
                BufferedReader in = new BufferedReader(new InputStreamReader(
                        connobj.getInputStream(), "utf-8"));// 防止乱码
                String inputLine = null;
                while ((inputLine = in.readLine()) != null) {
                    json.append(inputLine);
                }
                Message msg = Message.obtain();
                msg.obj = json.toString();
                myhandler.sendMessage(msg);
                in.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    private static class My_handler extends Handler{
        //Handler内存泄漏
        private final WeakReference<listenerdemo>mactivity;
        My_handler (listenerdemo activity){
            mactivity =new WeakReference<>(activity);
        }
        @Override
        public void handleMessage(Message msg) {
            listenerdemo activity= mactivity.get();
            String receive_data = msg.obj.toString().replace("[","").replace("]","");
            int count=searchCount(receive_data);
            if (count==0){
                String result="明日pm2.5为预测结果："+receive_data;
                activity.main_vw.setText(result);
            }
            if (count==1){
                String result="明后俩天pm2.5预测结果为："+receive_data;
                activity.main_vw.setText(result);
            }
            if (count>=2){
                String result="未来"+String.valueOf(count+1)+"天pm2.5预测结果为："+receive_data;
                activity.main_vw.setText(result);
            }
        }
    }
    public static int searchCount(String longStr) {
        // 服务器返回的数据为类似45,56,78,8的一串字符串,通过判断逗号出现的次数来判断返回单个数据的个数
        int count = 0;
        while (longStr.contains(",")) {
            count++;
            longStr = longStr.substring(longStr.indexOf(",") + 1);
                    }
                    return count; }

}
