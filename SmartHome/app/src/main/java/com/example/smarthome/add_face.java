package com.example.smarthome;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.Toast;

import androidx.activity.EdgeToEdge;
import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultCallback;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.contract.ActivityResultContracts;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

import com.bumptech.glide.Glide;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.material.progressindicator.LinearProgressIndicator;
import com.google.firebase.Firebase;
import com.google.firebase.FirebaseApp;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.OnProgressListener;
import com.google.firebase.storage.StorageReference;
import com.google.firebase.storage.UploadTask;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Random;
import java.util.UUID;

public class add_face extends AppCompatActivity {

    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference change_video = database.getReference("change_video");
    StorageReference storageReference;
    LinearProgressIndicator progressIndicator;
    Uri video;
    Button selectVideo,uploadVideo;
    ImageView imageView;
    EditText name;
    ImageButton back_faceid;

    ActivityResultLauncher<Intent> activityResultLauncher = registerForActivityResult(new ActivityResultContracts.StartActivityForResult(), new ActivityResultCallback<ActivityResult>() {
        @Override
        public void onActivityResult(ActivityResult result) {
            if (result.getResultCode() == RESULT_OK){
                if (result.getData() != null){
                    uploadVideo.setEnabled(true);
                    video = result.getData().getData();
                    Glide.with(add_face.this).load(video).into(imageView);
                } else {
                    Toast.makeText(add_face.this,"Please select a video",Toast.LENGTH_SHORT).show();
                }
            }
        }
    });

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_add_face);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        back_faceid = findViewById(R.id.back_faceid);
        back_faceid.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(add_face.this, MainActivity.class);
                startActivity(intent);
            }
        });

        FirebaseApp.initializeApp(this);
        name = findViewById(R.id.name);
        storageReference = FirebaseStorage.getInstance().getReference();


        imageView = findViewById(R.id.imageView);
        progressIndicator = findViewById(R.id.process);
        selectVideo = findViewById(R.id.selectVideo);
        uploadVideo = findViewById(R.id.uploadVideo);

        selectVideo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Intent.ACTION_PICK);
                intent.setType("video/");
                activityResultLauncher.launch(intent);
            }
        });

        uploadVideo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (name.getText().toString().isEmpty()) {
                    Toast.makeText(add_face.this,"Please enter a name",Toast.LENGTH_SHORT).show();
                } else
                    uploadVideo(video);
            }
        });
    }

    String CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    Random rand = new Random();
    SimpleDateFormat sdf = new SimpleDateFormat("yyMMddHHmmssSSS");
    public String get_rand(){
        StringBuilder sb = new StringBuilder();
        sb.append(sdf.format(new Date()));
//        for (int i=0; i<8; i++)
//            sb.append(CHARACTERS.charAt(rand.nextInt(CHARACTERS.length())));
        return sb.toString();
    }

    private void uploadVideo(Uri uri){
        String name_video = name.getText().toString() + "_" + get_rand();
        StorageReference reference = storageReference.child("video/" + name_video);
        reference.putFile(uri).addOnSuccessListener(new OnSuccessListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onSuccess(UploadTask.TaskSnapshot taskSnapshot) {
                Toast.makeText(add_face.this,"Video uploaded sussessfully", Toast.LENGTH_SHORT).show();

                change_video.setValue("ADD_" + name_video);

                //Refresh
                Intent intent = getIntent();
                finish();
                startActivity(intent);
            }
        }).addOnFailureListener(new OnFailureListener() {
            @Override
            public void onFailure(@NonNull Exception e) {
                Toast.makeText(add_face.this,"Failed to upload video", Toast.LENGTH_SHORT).show();
            }
        }).addOnProgressListener(new OnProgressListener<UploadTask.TaskSnapshot>() {
            @Override
            public void onProgress(@NonNull UploadTask.TaskSnapshot snapshot) {
                progressIndicator.setVisibility(View.VISIBLE);
                progressIndicator.setMax(Math.toIntExact(snapshot.getTotalByteCount()));
                progressIndicator.setProgress(Math.toIntExact(snapshot.getBytesTransferred()));
            }
        });
    }
}